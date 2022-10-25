import json
import os

import requests

from stock import Stock

HOST = 'yh-finance.p.rapidapi.com'
headers = {
    "Content-Type": "application/json",
    "X-RapidAPI-Key": os.environ['FINANCE_API_KEY'],
    "X-RapidAPI-Host": HOST
}


def get_stock_info(stock: str):
    full_uri = f'https://{HOST}/stock/v2/get-summary'
    params = {'symbol': stock}

    data = requests.get(full_uri, params=params, headers=headers).text
    if len(data) == 0:
        return None

    data = json.loads(data)
    symbol = data['symbol']

    return Stock(
        id=0,
        short_name=data['quoteType']['shortName'],
        long_name=data['quoteType']['longName'],

        symbol=symbol,
        sector=data['summaryProfile']['sector'],
        exchange=data['quoteType']['exchange'],
        timezone=data['quoteType']['exchangeTimezoneName'],
        currency=data['summaryDetail']['currency'],

        price=data['financialData']['currentPrice']['raw'],
        beta=data['summaryDetail']['beta']['raw'],

        dividend_yield=data['summaryDetail']['dividendYield']['raw'],
        ex_dividend_date=data['summaryDetail']['exDividendDate']['raw'],
        payout_ratio=data['summaryDetail']['payoutRatio']['raw'],

        debt_equity_ratio=data['financialData']['currentRatio']['raw'],
        # growth_estimate_5y=data['earningsTrend']['trend'][4]['growth']['raw']
    )
