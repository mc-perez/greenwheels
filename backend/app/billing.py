import math
from datetime import datetime
from decimal import Decimal


def minutes_out_ceiling(started_at: datetime, ended_at: datetime) -> int:
    seconds = (ended_at - started_at).total_seconds()
    if seconds <= 0:
        return 0
    return math.ceil(seconds / 60)


def compute_amount_owed(rate_at_checkout: Decimal, started_at: datetime, ended_at: datetime) -> Decimal:
    minutes = minutes_out_ceiling(started_at, ended_at)
    return rate_at_checkout * Decimal(minutes)
