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
    export let header = ["Name","Set","USD","USD (Foil)","Euro","Euro (Foil)","TIX"]
</script>

<script lang="ts">
    import { displayCardDashPopup } from "../assets/popup";

    import type { GetCard } from "../assets/responses";
    import { parseCurrency, CurrentCard } from "../assets/stores"
    import { database } from "../util/fetch_data"
    import Error from "./Error.svelte"
    export let col_span:number | string = 3
    export let row_span:number | string = 2
    export let group: string
    const connectURL = import.meta.env.VITE_CONNECTION;


    function ParseData(data:GetCard): Array<ResponseData> {
        let card_data = data.data
        let resp = []
        for (let i = 0; i < card_data.length; i++) {
            const card_info = card_data[i]
            let response_data = {
                "Name": card_info.name,
                "_set_short": card_info.set,
                "Set": `<i class="ss ml-4 text-2xl ss-${card_info.set} ss-rare"></i>`,
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
        if (header === "Name" || header === "_set_short") {
            return
        }
        else {
            return parseCurrency(value, header)
        }
    }

    function updateStore(newSetName: string, newID: string, newCardName: string) {
        $CurrentCard.set_name = newSetName
        $CurrentCard.id = newID
        $CurrentCard.card = newCardName
    }

</script>

{#await database(`${connectURL}/card/${group}`) then data}
<div style="grid-column: span {col_span} / span {col_span}; grid-row: span {row_span} / span {row_span}; ">


    <table class="bg-gray-50 dark:bg-gray-700 h-full component-theme flex flex-col" >

        <thead class="border-b-2 border-black/50 table table-fixed" style="width: calc(100% - .75em);">

            <tr class="text-xs uppercase text-gray-700 dark:text-gray-400 w-full">
                {#each header as titles}
                    <th scope="col" class="px-6 py-3 first:text-left text-right mx-0">
                        {titles}
                    </th>
                {/each}
            </tr>

        </thead>


            <tbody class="bg-white text-gray-200 dark:bg-gray-800 overflow-y-auto flex-auto basis-0 font-light scrollbar">
                {#each ParseData(data) as card_data}
                    <tr class="not-last:border-b-2 border-gray-700 w-full table table-fixed">
                        {#each header as data_type}
                            {#if data_type === "Name"}
                                <th scope="row" class="px-6 py-3 text-gray-900 dark:text-white text-left whitespace-preline">
                                    {card_data["Name"]}
                                </th>
                            {:else}
                            <td class="px-6 py-2 text-right whitespace-preline tabular-nums">
                                {@html parseRow(card_data[data_type], data_type)}
                            </td>
                            {/if}
                        {/each}
                    </tr>
                {/each}
            </tbody>


    </table>

</div>

{:catch}
<Error/>
{/await}
