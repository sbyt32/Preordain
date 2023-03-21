import type { ComponentType } from "svelte"
import { readable, writable, get } from "svelte/store"
import CardDash from "../lib/CardDash.svelte"
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


// Store
export const CurrentCard = writable({set_name: "vow", id: "38", card: "Thalia, Guardian of Thraben"})
export const connectURL = readable(import.meta.env.VITE_CONNECTION)
export const projectName = readable(import.meta.env.VITE_PROJECT)
const envIsTest = readable(import.meta.env.DEV)

function setProjectTitle() {
    const {subscribe, set, update} = writable('');
    let project = get(projectName)
    let projEnv = get(envIsTest)
    return {
        subscribe,
        set: (value:string) => {
            set(`${project} - ${value} ${projEnv ? "(Testing)":""}`)
        },
        clear: () => {
            set(`${project} - Home ${projEnv ? "(Testing)":""}`)
        }
    }
}

export const projectTitle = setProjectTitle()

// Change Popup status
function updateModal() {
    const store = writable(false)
    const component = writable(CardDash)

    return {
        ...store,
        toggle: () => store.update(n => !n) ,
        show: (value:ComponentType) => {
            store.set(true)
            component.set(value)
        },
        close: () => store.set(false),

    }
}

export const showPopup = updateModal()
