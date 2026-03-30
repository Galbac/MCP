from datetime import datetime, timezone


class ClockService:
    @staticmethod
    def now_iso() -> str:
        return datetime.now(timezone.utc).isoformat()