export interface BaseResponse {
    resp: string
    status: 200
    info? : {}
    data? : [{}] | {}
}

export interface PriceData {
    usd: number,
    usd_foil: number,
    euro: number,
    euro_foil: number,
    tix: number
}

interface MultipleCardData {
    name: string,
    set: string,
    set_full: string,
    id: string,
    last_updated: string
    prices: PriceData
}

export interface GetCard extends BaseResponse {
    resp: 'card_info'
    data: [MultipleCardData]
}

export interface GetCardGroup extends BaseResponse {
    resp: 'card_info',
    info: {
        group_name: string,
        description: string,
        cards_in_group: number
    },
    data: [MultipleCardData]

}

export interface SearchQuery extends BaseResponse {
    resp: 'search_query',
    data: [MultipleCardData]

}

export interface GetInventory extends BaseResponse {
    resp: "retrieve_inventory",
    data: [
      {
        name: string,
        set: string,
        quantity: number,
        condition: string,
        variant: string,
        avg_cost: number
      }
    ]
}

export interface GetPriceDate extends BaseResponse {
    resp: "price_data",
    data: [MultipleCardData]

}

export interface GetPriceSingle extends BaseResponse {
    resp: "price_data",
    data: {
        name: string,
        set: string,
        set_full: string,
        id: string,
        prices: [
            {
                date: string,
                usd: number,
                usd_change: string,
                usd_foil: number,
                usd_foil_change: string,
                euro: number,
                euro_change: string,
                euro_foil: number,
                euro_foil_change: string,
                tix: number,
                tix_change: string
            }
        ]
    }
}

export interface GetSalesRecent extends BaseResponse {
        resp: "recent_card_sales",
        data: [
        {
            "order_date": string
            "condition": string,
            "variant": string,
            "quantity": number,
            "buy_price": number,
            "ship_price": number
        }
        ]
}

export interface GetSalesDaily extends BaseResponse {
    resp: "daily_card_sales",
    data: [
        {
            "name": string,
            "set": string,
            "id": string,
            "sales": [
                {
                    "day": string,
                    "sales": number,
                    "avg_cost": number,
                    "day_change": string
                }
            ]
        }
    ]
}
