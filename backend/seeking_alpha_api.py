from typing import List

import requests

from config import SEEKING_ALPHA_HOST, SEEKING_ALPHA_API_KEY
from utils import chunks

headers = {
    "Content-Type": "application/json",
    "X-RapidAPI-Key": SEEKING_ALPHA_API_KEY,
    "X-RapidAPI-Host": SEEKING_ALPHA_HOST
}


def get_stock_symbol(symbol: str, exchange: str):
    if exchange.upper() == 'TSX':
        return symbol + ':CA'
    return symbol


def get_stocks_info(stocks: List[str]) -> list:
    full_uri = f'https://{SEEKING_ALPHA_HOST}/symbols/get-summary'
    grouped_stocks = chunks(stocks, 4)
    data = []

    for chunk in grouped_stocks:
        params = {'symbols': ','.join(chunk)}

        response_json = requests.get(full_uri, params=params, headers=headers).json()
        if len(response_json['data']) == 0:
            continue

        data.extend(response_json['data'])

    return data
