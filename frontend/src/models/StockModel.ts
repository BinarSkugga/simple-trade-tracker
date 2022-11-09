export class StockModel {
    id: number
    ws_id: string
    name: string

    type: string
    symbol: string
    currency: string
    exchange: string
    tags: string

    price: number

    can_use_fractional: boolean
    buyable: boolean

    eps: number
    pe: number
    beta: number
    high52: number
    low52: number
    ex_dividend_date: number
    dividend_yield: number


    constructor(id: number, ws_id: string, name: string, type: string, symbol: string, currency: string,
                exchange: string, tags: string, price: number, can_use_fractional: boolean, buyable: boolean,
                eps: number, pe: number, beta: number, high52: number, low52: number, ex_dividend_date: number,
                dividend_yield: number) {
        this.id = id;
        this.ws_id = ws_id;
        this.name = name;
        this.type = type;
        this.symbol = symbol;
        this.currency = currency;
        this.exchange = exchange;
        this.tags = tags;
        this.price = price;
        this.can_use_fractional = can_use_fractional;
        this.buyable = buyable;
        this.eps = eps;
        this.pe = pe;
        this.beta = beta;
        this.high52 = high52;
        this.low52 = low52;
        this.ex_dividend_date = ex_dividend_date;
        this.dividend_yield = dividend_yield;
    }
}