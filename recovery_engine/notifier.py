"""
Forensic Notification & Remote Alerting Engine
Dispatches real-time alerts to Discord, Telegram, LINE, and custom Webhooks
for long-running recovery jobs, critical SMART hardware failures, and thermal alarms.
"""

import json
import urllib.request
import urllib.parse
from typing import Optional, Dict

class AlertNotifier:
    """
    Zero-dependency Webhook & Chat Alert Dispatcher.
    """
    def __init__(
        self,
        webhook_url: Optional[str] = None,
        telegram_token: Optional[str] = None,
        telegram_chat_id: Optional[str] = None
    ):
        self.webhook_url = webhook_url
        self.telegram_token = telegram_token
        self.telegram_chat_id = telegram_chat_id
        self.enabled = bool(self.webhook_url or (self.telegram_token and self.telegram_chat_id))

    def send_alert(self, title: str, message: str, level: str = "INFO") -> bool:
        """
        Send formatted alert notification to configured endpoints.
        """
        if not self.enabled:
            return False

        icon = "🚀"
        if level == "CRITICAL" or level == "ERROR":
            icon = "🚨"
        elif level == "WARNING":
            icon = "⚠️"
        elif level == "SUCCESS":
            icon = "🎉"

        full_text = f"{icon} [{level}] {title}\n{message}"
        success = True

        # 1. Dispatch Webhook (Discord / Slack / Generic)
        if self.webhook_url:
            try:
                # Handle Discord formatted payload
                if "discord.com" in self.webhook_url or "discordapp.com" in self.webhook_url:
                    payload = {
                        "username": "Data Recovery Bot",
                        "content": f"**{icon} {title}**\n```{message}```"
                    }
                else:
                    payload = {
                        "text": full_text,
                        "title": title,
                        "level": level,
                        "message": message
                    }

                req_data = json.dumps(payload).encode("utf-8")
                req = urllib.request.Request(
                    self.webhook_url,
                    data=req_data,
                    headers={"Content-Type": "application/json", "User-Agent": "RecoveryEngine/2.0"}
                )
                with urllib.request.urlopen(req, timeout=10) as resp:
                    pass
            except Exception:
                success = False

        # 2. Dispatch Telegram Bot API
        if self.telegram_token and self.telegram_chat_id:
            try:
                tg_url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
                payload = {
                    "chat_id": self.telegram_chat_id,
                    "text": full_text,
                    "parse_mode": "HTML"
                }
                req_data = json.dumps(payload).encode("utf-8")
                req = urllib.request.Request(
                    tg_url,
                    data=req_data,
                    headers={"Content-Type": "application/json"}
                )
                with urllib.request.urlopen(req, timeout=10) as resp:
                    pass
            except Exception:
                success = False

        return success

    def notify_recovery_complete(
        self,
        source_device: str,
        total_files: int,
        total_mb: float,
        duration_sec: float,
        sensitive_count: int = 0,
        bad_sectors_count: int = 0
    ) -> bool:
        """
        Send summary notification when recovery job completes.
        """
        msg = (
            f"Device: {source_device}\n"
            f"Extracted: {total_files} files ({total_mb:.2f} MB)\n"
            f"Duration: {duration_sec:.1f} seconds\n"
            f"Sensitive Files: {sensitive_count}\n"
            f"Bad Sectors: {bad_sectors_count}"
        )
        return self.send_alert("Data Recovery Job Finished", msg, level="SUCCESS")
