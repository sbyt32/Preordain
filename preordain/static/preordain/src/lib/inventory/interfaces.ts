import type { BaseCardData } from "../../assets/interfaces";
import type { BaseResponse, PriceData } from "../../assets/responses";
export interface SingleCardData extends BaseCardData {
    uri: string
    last_updated: string
    prices: PriceData
}

export interface SingleCardResponse extends BaseResponse {
    resp: "card_info"
    data: SingleCardData
}

export interface InventoryBody {
    add_date: string
    uri: string
    qty: number
    buy_price: number
    card_condition: string
    card_variant: string
}

export interface InventoryData extends BaseCardData{
    add_date: string
    quantity: number
    card_condition: string
    card_variant: string
    avg_cost: number
    change: string
}

export interface InventoryResponse extends BaseResponse {
    resp: "inventory_data"
    data: InventoryData[]
}
