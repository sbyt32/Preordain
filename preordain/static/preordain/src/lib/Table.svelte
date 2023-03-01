<script context="module" lang="ts">
    export interface ResponseData {
        name: string
        set: string
        id: string
        usd: number
        usd_foil: number
        euro: number
        euro_foil: number
        tix: number
    }
    export let header = ["Name","Set","Collector No.","USD","USD (Foil)","Euro","Euro (Foil)","TIX"]
</script>

<script lang="ts">
    import type { GetCard } from "../assets/responses";
    import { parseCurrency, CurrentCard } from "../assets/functions"
    import { database } from "../fetch_data"

    function ParseData(data:GetCard): Array<ResponseData> {
        let card_data = data.data
        let resp = []
        for (let i = 0; i < card_data.length; i++) {
            const card_info = card_data[i]
            let response_data = {
                "Name": card_info.name,
                "_set_short": card_info.set,
                "Set": card_info.set_full,
                "Collector No.": card_info.id,
                "USD": card_info.prices.usd,
                "USD (Foil)": card_info.prices.usd_foil,
                "Euro": card_info.prices.euro,
                "Euro (Foil)": card_info.prices.euro_foil,
                "TIX": card_info.prices.tix,
            }
            resp.push(response_data)
        }
        return resp
    }

    function parseRow(value: string | number, header: string) {
        if (header === "Name") {
            return
        } else if (header === "_set_short") {
            return
        }
        else {
            return `<td class="px-6 py-4">
                        ${parseCurrency(value, header)}
            </td>`
        }
    }

    function updateStore(newSetName: string, newID: string) {
        $CurrentCard.set_name = newSetName
        $CurrentCard.id = newID
    }
</script>

{#await database('http://127.0.0.1:8000/api/card/') then data}
    <div class="rounded-lg bg-gray-50 dark:bg-gray-700">
        <table class="w-full text-sm text-left ">
            <thead class="table w-full table-fixed">
                <tr class="text-xs uppercase text-gray-700  dark:text-gray-400">
                    {#each header as titles}
                        <th scope="col" class="px-6 py-3">
                            {titles}
                        </th>
                    {/each}
                </tr>
            </thead>
            <tbody class="block h-[218px] overflow-y-scroll bg-white text-gray-200 dark:bg-gray-800">
                {#each ParseData(data) as card_data}
                    <tr class="table w-full table-fixed dark:border-gray-700 border-b content-evenly">
                        {#each header as data_type}
                            {#if data_type === "Name"}
                                <th scope="row" class="px-6 py-4 font-medium text-gray-900 dark:text-white text-left" on:click={() => updateStore(card_data["_set_short"], card_data["Collector No."])}>
                                    {card_data["Name"]}
                                </th>
                            {:else}
                                {@html parseRow(card_data[data_type], data_type)}
                            {/if}
                        {/each}
                    </tr>
                {/each}
            </tbody>
        </table>
    </div>
{/await}
