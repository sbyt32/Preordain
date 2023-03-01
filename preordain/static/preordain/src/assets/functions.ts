import { writable, type Updater } from "svelte/store"
export function parseCurrency(price:number | string, currency:string) {
    // Checks
    if (typeof price == "string") {
        return price
    } else if (price == null) {
        return `N/A`
    }

    if (currency.toLowerCase().includes("usd")) {
        let stuff = new Intl.NumberFormat("en-US", {style: 'currency', currency: 'USD'}).format(price)
        return stuff
    } else if (currency.toLowerCase().includes("euro")) {
        let stuff = new Intl.NumberFormat("de-DE", {style: 'currency', currency: 'EUR'}).format(price)
        return stuff
    } else {
        return `${price} TIX`
    }
}

export const CurrentCard = writable({set_name: "vow", id: "38"})
