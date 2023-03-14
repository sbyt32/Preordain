import type { ScryfallSearchResults } from "../assets/externalTypes";

export function onKeyPress(e: KeyboardEvent, str: string) {
    if (e.code === 'Enter') { console.log(str)};
}

export async function handleSubmit(cardToSearch: string) {
    let resp:ScryfallSearchResults[] = []
    console.log('hi');
    const searchQuery = await fetch(`https://api.scryfall.com/cards/search?q=${cardToSearch}`)
    const searchResults = await searchQuery.json()

    for (let i = 0; i < searchResults.data.length; i++) {
        const element = searchResults.data[i];
        resp = resp.concat({
                name: element.name,
                set: element.set.toUpperCase(),
                set_full: element.set_name,
                id: element.collector_number,
                uri: element.id,
                tcg_id: element.tcgplayer_id,
                prices: {
                    usd: element.prices.usd,
                    usd_foil: element.prices.usd_foil,
                    euro: element.prices.eur,
                    euro_foil: element.prices.eur_foil,
                    tix: element.prices.tix,
                }
        })
    }

    if (resp.length >= 1) {
        return resp
    }
}

export async function trackNewCard(params:ScryfallSearchResults) {

    const newCard = {
        "name": params.name,
        "set": params.set,
        "id": params.id,
        "uri": params.uri,
        "tcg_id": params.tcg_id,
        "new_search": true
    }

    await fetch('http://127.0.0.1:8000/api/tracker/add/', {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "write": "testing"
        },
        body: JSON.stringify(newCard)
    })
    .then((resp) => resp.json())
    .then((data) => {
        return data
    })

}
