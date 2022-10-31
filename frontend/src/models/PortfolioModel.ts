export class PortfolioEntry {
    id: number
    portfolio_id: number
    stock_id: number
    count: number
    strike: number
    date: number

    constructor(id: number, portfolio_id: number, stock_id: number, count: number, strike: number, date: number) {
        this.id = id;
        this.portfolio_id = portfolio_id;
        this.stock_id = stock_id;
        this.count = count;
        this.strike = strike
        this.date = date;
    }
}


export class PortfolioModel {
    id: number
    name: string
    user_id: number

    entries: Array<PortfolioEntry> = []


    constructor(id: number, name: string, user_id: number, entries: Array<PortfolioEntry>) {
        this.id = id;
        this.name = name;
        this.user_id = user_id;
        this.entries = entries;
    }
}