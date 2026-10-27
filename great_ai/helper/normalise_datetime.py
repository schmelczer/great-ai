from datetime import datetime, timezone


def normalise_datetime(value: datetime) -> datetime:
    """Interpret naive timestamps as UTC and normalize aware timestamps to UTC."""
    return (
        value.astimezone(timezone.utc).replace(tzinfo=None) if value.tzinfo else value
    )
