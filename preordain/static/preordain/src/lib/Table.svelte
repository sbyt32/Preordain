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
    import { displayCardDashPopup } from "../assets/popup";

    import type { GetCard } from "../assets/responses";
    import { parseCurrency, CurrentCard } from "../assets/stores"
    import { database } from "../util/fetch_data"
    import Error from "./Error.svelte"
    // export let col_span:number | string = 4
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
                "Set": `${card_info.set_full}<br><i class="ss text-xl ss-${card_info.set}"></i>`,
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
            return `<td class="" style="font-variant-numeric: tabular-nums">
                        ${parseCurrency(value, header)}
            </td>`
        }
    }

    function updateStore(newSetName: string, newID: string, newCardName: string) {
        $CurrentCard.set_name = newSetName
        $CurrentCard.id = newID
        $CurrentCard.card = newCardName
    }

</script>

{#await database(`${connectURL}/card/${group}`) then data}
<div
    class="shadow-2xl component-theme row-span-2 col-span-3">


    <table class="text-left w-full">
        <thead class=" border-b-gray-700 flex w-full border-b-4 ">
            <tr class="text-xs w-full uppercase text-gray-700 dark:text-gray-400 flex mb-4">
                {#each header as titles}
                    <th scope="col" class="first:text-left text-right p-4 grow">
                        {titles}
                    </th>
                {/each}
            </tr>
        </thead>



        <tbody class="bg-white text-gray-200 dark:bg-gray-800 rounded-lg scrollbar">
            {#each ParseData(data) as card_data}
                <tr class=" dark:border-gray-700 border-b text-sm">
                    {#each header as data_type}
                        {#if data_type === "Name"}
                            <th scope="row" class="text-ellipsis">
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
    <!-- <div class="row-span-2 col-span-2 w-full bg-gray-700">
        <table class="table-fixed ">
            <thead class=" w-full">
                <tr>
                    {#each header as titles}
                    <th>
                        {titles}
                    </th>
                    {/each}
                </tr>
            </thead>
            <tbody>
                {#each ParseData(data) as card_data}
                <tr class=" dark:border-gray-700 border-b text-sm">
                    {#each header as data_type}
                        {#if data_type === "Name"}
                            <th scope="row" class="text-ellipsis">
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
    </div> -->

</div>

{:catch}
<Error/>
{/await}
