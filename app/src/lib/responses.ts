import type { PriceData } from "./models";

export interface PriceResponse {
    date: string
    prices: PriceData
}
