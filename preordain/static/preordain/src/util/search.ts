
export type SearchResults = {
    name: string
    set: string
    set_full: string
    id: string
    uri: string
    prices: {
        usd: number | string
        usd_foil: number | string
        usd_etch: number | string
        euro: number | string
        euro_foil: number | string
        tix: number | string
    }
}

export function onKeyPress(e: KeyboardEvent, str: string) {
    if (e.code === 'Enter') { console.log(str)};
}
const connectURL = import.meta.env.VITE_CONNECTION;

export async function handleSubmit(cardToSearch: string) {
    console.log('hi');
    const searchQuery = await fetch(`${connectURL}/search/${cardToSearch}`)
    const searchResults = await searchQuery.json()
    if (searchQuery.ok) {
        return searchResults.data
    } else {
        throw new Error(searchResults);
    }

}

export async function trackNewCard(params:SearchResults) {

    let newCard = {
        "uri": params.uri,
    }

    await fetch(`${connectURL}/tracker/add/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "write": "testing"
        },
        body: JSON.stringify(newCard)
    })
}

export async function untrackOldCard(params:SearchResults) {

    let newCard = {
        "uri": params.uri,
    }

    await fetch(`${connectURL}/tracker/remove/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "write": "testing"
        },
        body: JSON.stringify(newCard)
    })
}
