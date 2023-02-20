import os
from datetime import datetime
from typing import Optional

from models.activity import Activity


def iso_to_epoch(iso: str, format: str = "%Y-%m-%d") -> Optional[int]:
    if not isinstance(iso, str):
        return None
    utc_time = datetime.strptime(iso, format)
    return int((utc_time - datetime(1970, 1, 1)).total_seconds())


def chunks(lst: list, sub_size: int):
    for i in range(0, len(lst), sub_size):
        yield lst[i:i + sub_size]


def create_dist_folder(path: str):
    if not os.path.exists(path):
        os.mkdir(path)


def get_activity_date(activity: dict) -> int:
    str_date = None
    if activity['object'] == 'dividend' and activity['effective_date'] is not None:
        str_date = activity['effective_date'].split('T')[0]
    elif activity['object'] == 'deposit' and activity['accepted_at'] is not None:
        str_date = activity['accepted_at'].split('T')[0]
    elif activity['object'] == 'order' and activity['completed_at'] is not None:
        str_date = activity['completed_at'].split('T')[0]
    else:
        return -1

    return iso_to_epoch(str_date)


def build_activity(activity: dict) -> Activity:
    if activity['object'] == 'deposit':
        return Activity(**{
            'id': None,
            'type': activity['object'],
            'date': get_activity_date(activity),

            'amount': activity['value']['amount'],
            'currency': activity['value']['currency'],
            'status': activity['status']
        })
    if activity['object'] == 'dividend':
        return Activity(**{
            'id': None,
            'type': activity['object'],
            'date': get_activity_date(activity),

            'amount': activity['net_cash']['amount'],
            'currency': activity['net_cash']['currency'],

            'symbol': activity['symbol']
        })
    if activity['object'] == 'order' and activity['status'] != 'cancelled':
        return Activity(**{
            'id': None,
            'type': activity['object'],
            'date': get_activity_date(activity),

            'amount': activity['account_value']['amount'] / activity['quantity'],
            'currency': activity['account_value']['currency'],

            'symbol': activity['symbol'],
            'status': activity['status'],
            'quantity': activity['quantity'],
            'security_id': activity['security_id'],
            'limit_price': activity['limit_price']['amount'],
            'order_type': activity['order_type'],
            'order_sub_type': activity['order_sub_type']
        })
