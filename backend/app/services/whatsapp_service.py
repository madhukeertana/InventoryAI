"""Stub WhatsApp Business API client for daily action feeds."""

from app.core.config import get_settings

settings = get_settings()


class WhatsAppService:
    def send_action_feed(self, phone: str, cards: list[dict]) -> dict:
        return {
            "sent": False,
            "phone": phone,
            "card_count": len(cards),
            "engine": "whatsapp-stub",
            "api_configured": bool(settings.whatsapp_api_token),
            "message": "Stub only — configure WHATSAPP_API_TOKEN to enable",
        }
