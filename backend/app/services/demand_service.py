"""Stub demand prediction hooks for Prophet / LightGBM."""


class DemandService:
    def estimate_days_of_cover(self, quantity: int, velocity_tag: str | None) -> int | None:
        daily = {
            "FAST": 8,
            "MEDIUM": 3,
            "SLOW": 1,
            "UNKNOWN": 2,
        }.get(velocity_tag or "UNKNOWN", 2)
        if daily <= 0:
            return None
        return max(0, quantity // daily)

    def forecast_sku(self, sku: str, horizon_days: int = 30) -> dict:
        return {
            "sku": sku,
            "horizon_days": horizon_days,
            "engine": "prophet-lightgbm-stub",
            "predicted_units": 42,
            "confidence": 0.0,
        }
