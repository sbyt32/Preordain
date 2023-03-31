import { database } from "../../util/fetch_data";
import type { InventoryBody, InventoryResponse, ResponseData } from "./interfaces";
import { parseCurrency, connectURL } from "../../assets/stores"
import { parsePercentage } from "../../util/parseValues";
import { get } from "svelte/store";
const verboseConditions = {
    NM: "Near Mint",
    LP: "Lightly Played",
    MP: "Moderately Played",
    HP: "Heavily Played",
    DMG: "Damaged"
}

const verboseVariants = {
    Normal : "Non-Foil",
    Foil : "Foil 🌟",
    Etched : "Etched",
}

function humanizeConditions(condition:string) {
    return verboseConditions[condition]
}

function humanizeVariants(variant:string) {
    return verboseVariants[variant]
}

export function parseRow(value: ResponseData, header: string) {
    switch (header) {
        case "Set":
            return `
                <div class="text-right font-normal group relative">
                    <i class="ss text-2xl ss-${value["_set_short"]} ss-rare"></i>
                    <div class="absolute left-12 -right-8 py-1 mt-8 px-2 z-10 w-full text-base inline-block text-white text-center bg-gray-700 border rounded-md invisible opacity-0 group-hover:visible group-hover:opacity-100 transition-opacity duration-500">
                        ${value[header]}
                    </div>
                </div>
            `
        case "Change":
            return parsePercentage(value[header])
        case "Cost":
            return parseCurrency(value[header], "USD")
        case "Condition":
            return humanizeConditions(value[header])
        case "Variant":
            return humanizeVariants(value[header])
        default:
            return `${value[header]}`
    }
}

export async function parseData() {

    let resp:ResponseData[] = []
    let data:InventoryResponse = await database(`${get(connectURL)}/inventory/?access=testing`)
    if (data)
    data.data.forEach(card => {
        resp.push(
            {
                "Name": card.name,
                "Set": card.set_full,
                "Collector No.": card.id,
                "Condition" : card.card_condition,
                "Variant" : card.card_variant,
                "Cost" : card.avg_cost,
                "Change" : card.change,
                "Quantity": card.quantity,
                "Add Date": card.add_date,
                "_set_short": card.set,
                "_uri": card.uri
            }
        )
    });
    return resp
}

export async function modifyInventory(cardsToUpdateArray:ResponseData[], route: string, method: string) {

    cardsToUpdateArray.forEach(async card => {

        if (Object.values(card).some(x => x === null || x === '')) {
            throw new Error("missing data");
        }

        let cardToRemoveData:InventoryBody = {
            add_date: card["Add Date"],
            uri: card["_uri"],
            qty: card["Quantity"],
            buy_price: card["Cost"],
            card_condition: card["Condition"],
            card_variant: card["Variant"]
        }
        setTimeout(async () =>
            await fetch(`${get(connectURL)}${route}`, {
                method,
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(cardToRemoveData)
                }
                ).then((data) => {
                    if (!data.ok) {
                        throw new Error("Bad Data!");
                    }
                }), 1000
        )

    });
}
