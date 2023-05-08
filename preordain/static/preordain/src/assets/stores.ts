import type { ComponentType } from "svelte"
import { readable, writable, get } from "svelte/store"
import CardDash from "../lib/CardDash.svelte"


// Store
export const CurrentCard = writable({
    set_name: "vow",
    id: "38",
    card: "Thalia, Guardian of Thraben",
    prices: {
        usd: "",
        usd_foil: "",
        euro: "",
        euro_foil: "",
        tix: ""
    }
})
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
    const store = writable({display: false, component: CardDash})

    return {
        ...store,
        // toggle: () => store.update(n => !n),
        show: (value:ComponentType) => {
            store.set({display: true, component: value})
        },
        close: () => store.set({display: false, component: CardDash}),

    }
}

export const showPopup = updateModal()

export const currentTab = writable('Home')
