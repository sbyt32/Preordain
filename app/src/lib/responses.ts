import type { PriceData, CardMetadata, CardLegalities } from "./models";

export interface PriceResponse {
    date: string
    prices: PriceData
}

export interface CardInfoResponse {
    scryfall_uri: string
    card_data: CardMetadata
    legalities: CardLegalities
    prices: PriceData
}
