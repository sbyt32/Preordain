<script context="module" lang="ts">
    export const headers = ["Name","Set","Condition","Variant","Quantity","Cost","Change","Add Date"]

    export interface ResponseData {
        "Name": string
        "Set": string
        "Collector No.": string
        "Condition" : string
        "Variant" : string
        "Cost" : number
        "Change": string
        "Quantity": number
        "Add Date": string
        "_set_short": string
    }
    export const connectURL = import.meta.env.VITE_CONNECTION;

</script>

<script lang="ts">
    import { database } from "../../util/fetch_data";
    import type { InventoryResponse } from "./interfaces";
    import { parseCurrency } from "../../assets/stores"
    import { parsePercentage } from "../../util/parseValues";
    import { humanizeConditions, humanizeVariants } from "./functions";
    export let col_span:number | string = 3
    export let row_span:number | string = 2

    async function parseData() {

        let resp:ResponseData[] = []
        let data:InventoryResponse = await database(`${connectURL}/inventory/?access=testing`)
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
                    "_set_short": card.set
                }
            )
        });
        return resp
    }


    function parseRow(value: ResponseData, header: string) {
        switch (header) {
            case "Set":
                return `
                    <div class="text-right font-normal group relative">
                        <i class="ss text-2xl ss-${value["_set_short"]} ss-rare"></i>
                        <div class="absolute left-12 -right-8 py-1 mt-8 px-2 z-10 w-full text-base inline-block text-white text-center bg-gray-700 border rounded-md w-full invisible opacity-0 group-hover:visible group-hover:opacity-100 transition-opacity duration-500">
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
</script>


<div style="grid-column: span {col_span} / span {col_span}; grid-row: span {row_span} / span {row_span};" class="">


    <table class="bg-gray-50 dark:bg-gray-700 h-full component-theme rounded-b-md flex flex-col">

        <thead class="border-b-2 border-black/50 table table-fixed" style="width: calc(100% - .75em);">

            <tr class="text-xs uppercase text-gray-700 dark:text-gray-400 w-full">
                {#each headers as titles}
                    <th scope="col" class="px-6 py-3 first:text-left text-right mx-0">
                        {titles}
                    </th>
                {/each}
            </tr>

        </thead>

        <tbody class="bg-white text-gray-200 dark:bg-gray-800 overflow-y-auto grow font-normal scrollbar rounded-b-lg">
            {#await parseData()}
            <tr class="not-last:border-b-2 border-gray-700 w-full table table-fixed">
                {#each headers as data_type}
                    {#if data_type === "Name"}
                        <th scope="row" class="px-6 py-3 text-gray-900 dark:text-white text-left cursor-pointer hover:text-blue-400 transition-colors">
                        Loading...
                        </th>
                    {:else}
                        <td class="px-6 py-2 text-right whitespace-preline tabular-nums">
                        Loading...
                        </td>
                    {/if}
                {/each}
            </tr>

            {:then data}

                {#each data as card_data}
                    <tr class="not-last:border-b-2 border-gray-700 w-full table table-fixed">
                        {#each headers as data_type}
                            {#if data_type === "Name"}
                                <th scope="row" class="px-6 py-3 text-gray-900 dark:text-white text-left whitespace-preline cursor-pointer hover:text-blue-400 transition-colors">
                                    {card_data["Name"]}
                                </th>
                            {:else}
                            <td class="px-6 py-2 whitespace-preline text-right">
                                {@html parseRow(card_data, data_type)}
                            </td>
                            {/if}
                        {/each}
                    </tr>
                {/each}
            {/await}
        </tbody>



    </table>

</div>
