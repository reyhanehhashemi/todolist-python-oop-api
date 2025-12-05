"""
Timezone utilities for Tehran (Asia/Tehran) timezone management.
"""

from datetime import datetime
from zoneinfo import ZoneInfo

TEHRAN_TZ = ZoneInfo("Asia/Tehran")


def get_tehran_now() -> datetime:
    """
    Get current datetime in Tehran timezone (naive, no offset).

    Returns:
        datetime: Current time in Tehran without timezone info

    Example:
        >>> now = get_tehran_now()
        >>> print(now)
        2025-12-06 12:52:33.123456
    """
    # ✅ اول UTC بگیر، بعد به تهران تبدیل کن، بعد naive کن
    utc_now = datetime.now(ZoneInfo("UTC"))
    tehran_aware = utc_now.astimezone(TEHRAN_TZ)
    return tehran_aware.replace(tzinfo=None)  # ✅ حذف timezone


def to_tehran(dt: datetime) -> datetime:
    """
    Convert any datetime to Tehran timezone (naive, no offset).

    Args:
        dt: Datetime object (can be naive or aware)

    Returns:
        datetime: Datetime converted to Tehran timezone without offset

    Example:
        >>> from datetime import datetime
        >>> utc_time = datetime(2025, 12, 6, 9, 22, 33)
        >>> tehran_time = to_tehran(utc_time)
        >>> print(tehran_time)
        2025-12-06 12:52:33
    """
    if dt is None:
        return None

    # If datetime is naive, assume it's UTC
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=ZoneInfo("UTC"))

    # Convert to Tehran timezone and remove offset
    tehran_aware = dt.astimezone(TEHRAN_TZ)
    return tehran_aware.replace(tzinfo=None)  # ✅ حذف timezone


def convert_to_tehran_naive(dt: datetime) -> datetime:
    """
    Convert any datetime to Tehran timezone (naive) for database storage.

    Args:
        dt: Datetime object (can be naive or aware)

    Returns:
        datetime: Naive datetime in Tehran timezone

    Example:
        >>> from datetime import datetime
        >>> dt = datetime(2025, 12, 7, 14, 0, 0)
        >>> naive = convert_to_tehran_naive(dt)
        >>> print(naive)
        2025-12-07 14:00:00
    """
    if dt is None:
        return None

    # Already naive? Just return it
    if dt.tzinfo is None:
        return dt

    # Has timezone? Convert to Tehran and strip timezone
    tehran_aware = dt.astimezone(TEHRAN_TZ)
    return tehran_aware.replace(tzinfo=None)
