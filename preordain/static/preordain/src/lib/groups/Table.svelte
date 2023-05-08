<script context="module" lang="ts">
    export let header = ["Name","Set","USD","USD (Foil)","Euro","Euro (Foil)","TIX"]

    export interface ResponseData {
        "Name": string
        "Set": string
        "Collector No.": string
        "USD": number
        "USD (Foil)": number
        "Euro": number
        "Euro (Foil)": number
        "TIX": number
        "_set_short": string
    }
</script>

<script lang="ts">

    import { updateCardDash } from "../../util/updateCardDashValue"
    import { parseCurrency } from "../../util/dataFormatter"
    import type { GetCardGroup} from "./interfaces"
    export let col_span:number | string = 3
    export let row_span:number | string = 2
    export let groupData:GetCardGroup;


    function parseData(data:GetCardGroup): Array<ResponseData> {
        let card_data = data.data
        let resp:ResponseData[] = []
        card_data.forEach(card => {
            resp.push({
                "Name": card.name,
                "Set": card.set_full,
                "Collector No.": card.id,
                "USD": card.prices.usd,
                "USD (Foil)": card.prices.usd_foil,
                "Euro": card.prices.euro,
                "Euro (Foil)": card.prices.euro_foil,
                "TIX": card.prices.tix,
                "_set_short": card.set
            })
        });
        return resp
    }



    function parseRow(value: ResponseData, header: string) {
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
            default:
                return parseCurrency(value[header], header)
        }
    }

</script>

<div style="grid-column: span {col_span} / span {col_span}; grid-row: span {row_span} / span {row_span};">


    <table class="bg-gray-50 dark:bg-gray-700 h-full component-theme rounded-b-md flex flex-col" >

        <thead class="border-b-2 border-black/50 table table-fixed" style="width: calc(100% - .75em);">

            <tr class="text-xs uppercase text-gray-700 dark:text-gray-400 w-full">
                {#each header as titles}
                    <th scope="col" class="px-6 py-3 first:text-left text-right mx-0">
                        {titles}
                    </th>
                {/each}
            </tr>

        </thead>

            <tbody class="bg-white text-gray-200 dark:bg-gray-800 overflow-y-auto grow font-light scrollbar rounded-b-lg">

                {#each parseData(groupData) as card_data}
                    <tr class="not-last:border-b-2 border-gray-700 w-full table table-fixed">
                        {#each header as data_type}
                            {#if data_type === "Name"}
                                <th scope="row" class="px-6 py-3 text-gray-900 dark:text-white text-left cursor-pointer hover:text-blue-400 transition-colors" on:click={() => updateCardDash(card_data)}>
                                    {card_data["Name"]}
                                </th>
                            {:else}
                            <td class="px-6 py-2 text-right whitespace-preline tabular-nums">
                                {@html parseRow(card_data, data_type)}
                            </td>
                            {/if}
                        {/each}
                    </tr>
                {/each}

            </tbody>


    </table>

</div>
