<script context="module" lang="ts">
    export const headers = ["Name","Set","Condition","Variant","Quantity","Cost","Change","Add Date"]

</script>

<script lang="ts">
    import { onMount, createEventDispatcher } from "svelte";
    import { parseRow, parseData } from "./functions";
    import type { ResponseData } from "./interfaces";

    export let selected = []
    let inventoryData:ResponseData[] = [];

    function selectAll() {
        selected = allSelected ? [] : [...inventoryData]
    }

    onMount(async () => {
        inventoryData = await parseData()
    })

	const dispatch = createEventDispatcher();

    function dispatchSelectAll() {
        dispatch("selectAll", {
            'select': selectAll()
        });
    }

    $: allSelected = inventoryData.length === selected.length
</script>

            <tbody class="bg-gray-800 overflow-y-auto grow font-normal scrollbar rounded-b-lg">

                {#each inventoryData as card_data, i}
                    <tr class="not-last:border-b-2 border-gray-700 w-full table table-fixed">

                        <td class="px-6 py-3 text-left mx-0 w-4">
                            <input type="checkbox" class=" text-blue-600 rounded bg-gray-700 " bind:group={selected} value={card_data}>
                        </td>

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

            </tbody>
