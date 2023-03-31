import { CurrentCard } from "../assets/stores"

export function updateCardDash(card_data) {
    CurrentCard.set({
        set_name : card_data["_set_short"],
        id : card_data["Collector No."],
        card : card_data["Name"]
    })
}
