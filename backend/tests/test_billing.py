from datetime import datetime, timezone
from decimal import Decimal

from app.billing import compute_amount_owed, minutes_out_ceiling


def test_minutes_out_ceiling_ninety_seconds_is_two():
    start = datetime(2026, 6, 1, 12, 0, 0, tzinfo=timezone.utc)
    end = datetime(2026, 6, 1, 12, 1, 30, tzinfo=timezone.utc)
    assert minutes_out_ceiling(start, end) == 2


def test_amount_owed_one_fifty_per_minute_two_minutes():
    start = datetime(2026, 6, 1, 12, 0, 0, tzinfo=timezone.utc)
    end = datetime(2026, 6, 1, 12, 1, 30, tzinfo=timezone.utc)
    assert compute_amount_owed(Decimal("150"), start, end) == Decimal("300")
