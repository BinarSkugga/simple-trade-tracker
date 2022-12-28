import os
from datetime import datetime
from typing import Optional


def iso_to_epoch(iso: str) -> Optional[int]:
    if not isinstance(iso, str):
        return None
    utc_time = datetime.strptime(iso, "%Y-%m-%d")
    return int((utc_time - datetime(1970, 1, 1)).total_seconds())


def chunks(lst: list, sub_size: int):
    for i in range(0, len(lst), sub_size):
        yield lst[i:i + sub_size]


def create_dist_folder(path: str):
    if not os.path.exists(path):
        os.mkdir(path)
