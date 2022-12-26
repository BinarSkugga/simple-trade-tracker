import type {StockModel} from "@/models/StockModel";

export class PositionModel {
    id: number
    ws_id: string

    quantity: number
    sellable_quantity: number
    book_value: number
    market_value: number

    stock?: StockModel

    constructor(id: number, ws_id: string, quantity: number, sellable_quantity: number, book_value: number, market_value: number) {
        this.id = id;
        this.ws_id = ws_id;
        this.quantity = quantity;
        this.sellable_quantity = sellable_quantity;
        this.book_value = book_value;
        this.market_value = market_value;
    }
}
