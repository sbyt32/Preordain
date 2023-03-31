import CardDash from "../lib/CardDash.svelte"
import { CurrentCard, showPopup } from "./stores"


export function displayCardDashPopup(card_data) {
    CurrentCard.set({
        set_name : card_data["set"],
        id : card_data["id"],
        card : card_data["name"]
    })
    showPopup.show(CardDash)
}
