export class StockModel {
    id: number
    ws_id: string
    name: string

    type: string
    symbol: string
    currency: string
    exchange: string
    price: number

    can_use_fractional: boolean
    buyable: boolean
    limited: boolean

    eps: number
    pe: number
    high52: number
    low52: number
    div_ex_date: number
    div_yield: number
    div_distribution: string

    sector: string


    constructor(id: number, ws_id: string, name: string, type: string, symbol: string, currency: string,
                exchange: string, price: number, can_use_fractional: boolean, buyable: boolean, limited: boolean,
                eps: number, pe: number, high52: number, low52: number, div_ex_date: number,
                div_yield: number, div_distribution: string, sector: string) {
        this.id = id;
        this.ws_id = ws_id;
        this.name = name;
        this.type = type;
        this.symbol = symbol;
        this.currency = currency;
        this.exchange = exchange;
        this.price = price;
        this.can_use_fractional = can_use_fractional;
        this.buyable = buyable;
        this.limited = limited;
        this.eps = eps;
        this.pe = pe;
        this.high52 = high52;
        this.low52 = low52;
        this.div_ex_date = div_ex_date;
        this.div_yield = div_yield;
        this.div_distribution = div_distribution
        this.sector = sector
    }
}