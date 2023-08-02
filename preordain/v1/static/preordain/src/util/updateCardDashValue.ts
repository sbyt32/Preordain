import { CurrentCard } from "../assets/stores"

export function updateCardDash(card_data) {
    CurrentCard.set({
        set_name : card_data["_set_short"],
        id : card_data["Collector No."],
        card : card_data["Name"],
        prices: {
            usd: card_data["USD"],
            usd_foil: card_data["USD (Foil)"],
            euro: card_data["Euro"],
            euro_foil: card_data["Euro (Foil)"],
            tix: card_data["TIX"]
        }
    })
}
