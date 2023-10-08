import { database } from '../../lib/connection';
export interface queryCard {
    set: string
    id: string
}

interface chartPrice {
    Date: Date
    Type: string
    Currency: string
    Price: string | number | null
}
export async function processPriceData(query:queryCard) {
    let data = await database(`price/${query.set}/${query.id}?days=30`)



    let priceData:chartPrice[] = []
    data.forEach(e => {
        let currentDate = new Date(e.date)
        priceData.push(
            { "Date": currentDate, "Type": "USD", "Currency": "USD", "Price":  e.prices.usd },
            { "Date": currentDate, "Type": "USD (Foil)", "Currency": "USD", "Price": (e.prices.usd_foil != null ? e.prices.usd_foil : null) },
            { "Date": currentDate, "Type": "USD (Etched)", "Currency": "USD", "Price": e.prices.usd_etch },
            // { "Date": new Date(e.date), "Type": "Euro", "Price": e.prices.euro },
            // { "Date": new Date(e.date), "Type": "Euro (Foil)", "Price": e.prices.euro_foil },
            // { "Date": new Date(e.date), "Type": "Tickets", "Price": (e.prices.tix != null ? e.prices.tix.toLocaleString("en-US", {style: "currency", currency: "USD"}) : null)},
        )
    });

    return priceData
}
