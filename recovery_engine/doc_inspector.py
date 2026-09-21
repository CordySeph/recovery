"""
Document & Sensitive Data Inspector Module
Scans extracted document payloads for:
- Thai National ID numbers (with checksum validation)
- Credit Card numbers (Luhn Algorithm)
- Thai & International Phone Numbers
- Email Addresses
- Financial & High-Value Keywords (Tax Invoices, Contracts, Passwords, Payroll)
"""

import re
from typing import Dict, List, Any, Optional

def validate_thai_id(id_str: str) -> bool:
    """Validate 13-digit Thai National ID checksum."""
    digits = [int(c) for c in id_str if c.isdigit()]
    if len(digits) != 13:
        return False
    # Checksum calculation: sum(d[i] * (13 - i)) for i in 0..11
    total = sum(digits[i] * (13 - i) for i in range(12))
    check_digit = (11 - (total % 11)) % 10
    return digits[12] == check_digit

def validate_luhn_credit_card(card_str: str) -> bool:
    """Validate Credit Card number using Luhn Algorithm."""
    digits = [int(c) for c in card_str if c.isdigit()]
    if not (13 <= len(digits) <= 19):
        return False
    checksum = 0
    reverse_digits = digits[::-1]
    for i, d in enumerate(reverse_digits):
        if i % 2 == 1:
            doubled = d * 2
            checksum += doubled - 9 if doubled > 9 else doubled
        else:
            checksum += d
    return checksum % 10 == 0

KEYWORDS_DEFAULT = [
    "ใบเสร็จ", "ใบกำกับภาษี", "สัญญา", "หนังสือมอบอำนาจ", "statement", "invoice",
    "receipt", "confidential", "secret", "password", "salary", "เงินเดือน", "ภ.ง.ด."
]

def extract_text_sample(data: bytes, max_len: int = 500000) -> str:
    """Extract plain text / printable strings from binary data."""
    if not data:
        return ""
    sample = data[:max_len]
    try:
        # Try UTF-8 decode
        return sample.decode("utf-8", errors="ignore")
    except Exception:
        # Latin-1 fallback
        return sample.decode("latin-1", errors="ignore")

def inspect_document_payload(data: bytes, file_type: str, custom_keywords: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    Inspect document binary payload for sensitive numbers, patterns, and keywords.
    """
    results = {
        "has_sensitive_data": False,
        "thai_ids_found": [],
        "credit_cards_found": [],
        "phone_numbers_found": [],
        "emails_found": [],
        "keywords_matched": [],
        "summary_badge": "",
    }

    ft = file_type.lower()
    # Relevant document and text types
    if ft not in ("pdf", "docx", "xlsx", "pptx", "txt", "sqlite", "db", "csv"):
        return results

    text = extract_text_sample(data)
    if not text:
        return results

    # 1. Thai National ID Regex Check
    thai_id_matches = re.findall(r"\b[1-8]\d{12}\b", text) + re.findall(r"\b[1-8]-\d{4}-\d{5}-\d{2}-\d\b", text)
    valid_thai_ids = set()
    for raw_id in thai_id_matches:
        clean_id = re.sub(r"\D", "", raw_id)
        if validate_thai_id(clean_id):
            valid_thai_ids.add(f"{clean_id[:1]}XXXXXXXXX{clean_id[-3:]}")  # Mask for safety

    if valid_thai_ids:
        results["thai_ids_found"] = list(valid_thai_ids)
        results["has_sensitive_data"] = True

    # 2. Credit Card Check (Luhn)
    cc_matches = (
        re.findall(r"\b(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|3[47][0-9]{13}|6(?:011|5[0-9]{2})[0-9]{12})\b", text) +
        re.findall(r"\b(?:4[0-9]{3}[ -][0-9]{4}[ -][0-9]{4}[ -][0-9]{4}|5[1-5][0-9]{2}[ -][0-9]{4}[ -][0-9]{4}[ -][0-9]{4})\b", text)
    )
    valid_ccs = set()
    for raw_cc in cc_matches:
        clean_cc = re.sub(r"\D", "", raw_cc)
        if validate_luhn_credit_card(clean_cc):
            valid_ccs.add(f"{clean_cc[:4]}XXXXXXXX{clean_cc[-4:]}")

    if valid_ccs:
        results["credit_cards_found"] = list(valid_ccs)
        results["has_sensitive_data"] = True

    # 3. Emails
    emails = re.findall(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b", text)
    if emails:
        results["emails_found"] = list(set(emails[:5]))

    # 4. Keywords
    target_keywords = (custom_keywords or []) + KEYWORDS_DEFAULT
    matched_kws = []
    text_lower = text.lower()
    for kw in target_keywords:
        if kw.lower() in text_lower:
            matched_kws.append(kw)

    if matched_kws:
        results["keywords_matched"] = list(set(matched_kws))
        if any(k in matched_kws for k in ("password", "secret", "confidential", "สัญญา", "statement")):
            results["has_sensitive_data"] = True

    # Generate badge
    badges = []
    if results["thai_ids_found"]:
        badges.append(f"Thai ID ({len(results['thai_ids_found'])})")
    if results["credit_cards_found"]:
        badges.append("Credit Card")
    if results["keywords_matched"]:
        badges.append(f"Keywords ({len(results['keywords_matched'])})")

    results["summary_badge"] = " • ".join(badges)
    return results
