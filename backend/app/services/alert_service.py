from sqlalchemy.orm import Session
from app.models import Alert
from app.core.config import settings
import httpx
from datetime import datetime


class AlertService:
    def __init__(self, db: Session):
        self.db = db

    async def send_alert(self, alert: Alert) -> int:
        recipients_count = 0

        if alert.channel == "sms" and settings.TWILIO_ACCOUNT_SID:
            recipients_count = await self._send_sms(alert)
        elif alert.channel == "whatsapp" and settings.TWILIO_ACCOUNT_SID:
            recipients_count = await self._send_whatsapp(alert)

        alert.status = "sent" if recipients_count > 0 else "failed"
        alert.sent_at = datetime.utcnow()
        self.db.commit()

        return recipients_count

    async def _send_sms(self, alert: Alert) -> int:
        if not settings.TWILIO_ACCOUNT_SID or not settings.TWILIO_AUTH_TOKEN:
            return 0

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"https://api.twilio.com/2010-04-01/Accounts/{settings.TWILIO_ACCOUNT_SID}/Messages.json",
                    auth=(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN),
                    data={
                        "Body": f"{alert.title}\n\n{alert.message}",
                        "To": "+254700000000",
                        "From": "+15005550006"
                    }
                )

                if response.status_code in (200, 201):
                    return 1

        except Exception as e:
            print(f"SMS send failed: {e}")

        return 0

    async def _send_whatsapp(self, alert: Alert) -> int:
        return await self._send_sms(alert)