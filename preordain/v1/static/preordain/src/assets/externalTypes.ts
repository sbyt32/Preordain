import type { PriceData } from "./responses"

export interface ScryfallSearch {
    object: string
    total_cards: string
    has_more: boolean
    data: []
}

export type ScryfallSearchResults = {
    name: string
    set: string
    set_full: string
    id: string
    uri: string
    tcg_id: string
    prices: {
        usd: number | string
        usd_foil: number | string
        euro: number | string
        euro_foil: number | string
        tix: number | string
    }
}
