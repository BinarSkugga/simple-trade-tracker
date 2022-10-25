export class StockModel {
    short_name: string
    long_name: string

    symbol: string
    sector: string
    exchange: string
    timezone: string
    currency: string

    price: number
    beta: number  // lower than 2

    dividend_yield: number  // as high as possible
    ex_dividend_date: number
    payout_ratio: number  // between 0.3 to 0.5

    debt_equity_ratio: number  // lower than 2
    // growth_estimate_5y: number  // between 0.05 and 0.15

    monthly_return: number


    constructor(short_name: string, long_name: string, symbol: string, sector: string, exchange: string,
                timezone: string, currency: string, price: number, beta: number, dividend_yield: number,
                ex_dividend_date: number, payout_ratio: number, debt_equity_ratio: number, monthly_return: number) {
        this.short_name = short_name;
        this.long_name = long_name;
        this.symbol = symbol;
        this.sector = sector;
        this.exchange = exchange;
        this.timezone = timezone;
        this.currency = currency;
        this.price = price;
        this.beta = beta;
        this.dividend_yield = dividend_yield;
        this.ex_dividend_date = ex_dividend_date;
        this.payout_ratio = payout_ratio;
        this.debt_equity_ratio = debt_equity_ratio;
        this.monthly_return = monthly_return;
    }
}