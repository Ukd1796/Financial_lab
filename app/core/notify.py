# app/core/notify.py
#
# Email notification via Gmail SMTP.
# Requires env vars:
#   EMAIL_FROM         — sender Gmail address
#   EMAIL_TO           — recipient address (can be same as FROM)
#   EMAIL_APP_PASSWORD — Gmail App Password (not your login password)
#                        Generate at: Google Account → Security → App Passwords
#
# Usage:
#   from app.core.notify import send_email
#   send_email("Subject", "Body text")

import os
import smtplib
from email.mime.text import MIMEText


def send_email(subject: str, body: str) -> bool:
    """Send an email via Gmail SMTP. Returns True on success, False on failure."""
    from_addr = os.environ.get("EMAIL_FROM", "")
    to_addr   = os.environ.get("EMAIL_TO", "")
    password  = os.environ.get("EMAIL_APP_PASSWORD", "")

    if not all([from_addr, to_addr, password]):
        print("  [Notify] Email not configured — skipping (set EMAIL_FROM, EMAIL_TO, EMAIL_APP_PASSWORD)")
        return False

    msg = MIMEText(body, "plain")
    msg["Subject"] = subject
    msg["From"]    = from_addr
    msg["To"]      = to_addr

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=15) as server:
            server.login(from_addr, password)
            server.sendmail(from_addr, [to_addr], msg.as_string())
        print(f"  [Notify] Email sent → {to_addr}")
        return True
    except Exception as exc:
        print(f"  [Notify] Email failed: {exc}")
        return False
