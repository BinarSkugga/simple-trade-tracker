from datetime import datetime
from typing import Optional


def iso_to_epoch(iso: str) -> Optional[int]:
    if not isinstance(iso, str):
        return None
    utc_time = datetime.strptime(iso, "%Y-%m-%dT%H:%M:%SZ")
    return int((utc_time - datetime(1970, 1, 1)).total_seconds())
