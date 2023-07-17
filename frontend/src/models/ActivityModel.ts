export class ActivityModel {
    id: number
    type: string
    date: number

    amount: number
    currency: string

    symbol?: string = undefined
    status?: string = undefined
    quantity?: number = undefined
    security_id?: string = undefined
    limit_price?: number = undefined
    order_type?: string = undefined
    order_sub_type?: string = undefined
    auto_order_type?: string = undefined


    constructor(id: number, type: string, date: number, amount: number, currency: string, symbol: string, status: string,
                quantity: number, security_id: string, limit_price: number, order_type: string,
                order_sub_type: string, auto_order_type: string) {
        this.id = id;
        this.type = type;
        this.date = date;
        this.amount = amount;
        this.currency = currency;
        this.status = status;
        this.quantity = quantity;
        this.security_id = security_id;
        this.limit_price = limit_price;
        this.order_type = order_type;
        this.order_sub_type = order_sub_type;
        this.auto_order_type = auto_order_type;
    }
}