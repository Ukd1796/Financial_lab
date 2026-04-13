# app/core/notify.py
#
# Email notifications. Two backends, tried in order:
#
# 1. Resend HTTP API (recommended for Railway / any container platform)
#      RESEND_API_KEY — API key from resend.com (free tier: 3k emails/month)
#      EMAIL_FROM     — verified sender address in your Resend account
#      EMAIL_TO       — recipient address
#
# 2. Gmail SMTP fallback (works locally; Railway blocks SMTP ports)
#      EMAIL_FROM         — Gmail address
#      EMAIL_TO           — recipient address
#      EMAIL_APP_PASSWORD — Gmail App Password
#                           Generate at: Google Account → Security → App Passwords
#
# Usage:
#   from app.core.notify import send_email
#   send_email("Subject", "Body text")

import os
import smtplib
from email.mime.text import MIMEText


def _send_via_resend(subject: str, body: str, from_addr: str, to_addr: str, api_key: str) -> bool:
    import requests
    resp = requests.post(
        "https://api.resend.com/emails",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={"from": from_addr, "to": [to_addr], "subject": subject, "text": body},
        timeout=15,
    )
    if resp.status_code == 200:
        print(f"  [Notify] Email sent via Resend → {to_addr}")
        return True
    print(f"  [Notify] Resend failed: {resp.status_code} {resp.text}")
    return False


def _send_via_smtp(subject: str, body: str, from_addr: str, to_addr: str, password: str) -> bool:
    msg = MIMEText(body, "plain")
    msg["Subject"] = subject
    msg["From"]    = from_addr
    msg["To"]      = to_addr
    # Try STARTTLS (587) first, then SSL (465)
    for port, use_ssl in [(587, False), (465, True)]:
        try:
            if use_ssl:
                ctx = smtplib.SMTP_SSL("smtp.gmail.com", port, timeout=15)
            else:
                ctx = smtplib.SMTP("smtp.gmail.com", port, timeout=15)
                ctx.starttls()
            with ctx as server:
                server.login(from_addr, password)
                server.sendmail(from_addr, [to_addr], msg.as_string())
            print(f"  [Notify] Email sent via SMTP:{port} → {to_addr}")
            return True
        except Exception as exc:
            print(f"  [Notify] SMTP:{port} failed: {exc}")
    return False


def send_email(subject: str, body: str) -> bool:
    """Send an email. Tries Resend API first, falls back to Gmail SMTP."""
    from_addr  = os.environ.get("EMAIL_FROM", "")
    to_addr    = os.environ.get("EMAIL_TO", "")
    resend_key = os.environ.get("RESEND_API_KEY", "")
    password   = os.environ.get("EMAIL_APP_PASSWORD", "")

    if not all([from_addr, to_addr]):
        print("  [Notify] Email not configured — skipping (set EMAIL_FROM, EMAIL_TO)")
        return False

    if resend_key:
        return _send_via_resend(subject, body, from_addr, to_addr, resend_key)

    if password:
        return _send_via_smtp(subject, body, from_addr, to_addr, password)

    print("  [Notify] No email backend configured — set RESEND_API_KEY or EMAIL_APP_PASSWORD")
    return False
