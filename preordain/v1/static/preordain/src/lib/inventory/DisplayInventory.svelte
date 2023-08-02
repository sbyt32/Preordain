<script context="module" lang="ts">
    export const headers = ["Name","Set","Condition","Variant","Quantity","Cost","Change","Add Date"]

</script>

<script lang="ts">
    import { onMount } from "svelte";
    import { fly } from "svelte/transition";

    import { modifyInventory, parseRow, parseData } from "./functions";
    import type { ResponseData } from "./interfaces";
    import { link, push } from "svelte-spa-router";
    export let col_span:number | string = 3
    export let row_span:number | string = 2

    let refresh = {}
    const restart = () => refresh = {}
    let selected = [];
    let inventoryData:ResponseData[] = [];

    function selectAll() {
        selected = allSelected ? [] : [...inventoryData]
    }

    onMount(async () => {
        inventoryData = await parseData()
    })

    $: allSelected = inventoryData.length === selected.length
</script>


<div style="grid-column: span {col_span} / span {col_span}; grid-row: span {row_span} / span {row_span};" >

    <table class="h-full component-theme rounded-b-md flex flex-col">

        <thead class="bg-gray-700 border-b-2 border-black/50 table table-fixed" style="width: calc(100% - .75em);">

            <tr class="text-xs uppercase text-gray-700 dark:text-gray-400 w-full">

                <td class="px-6 py-3 text-left mx-0 w-4">
                    <input type="checkbox" class=" text-blue-600 rounded bg-gray-700 " on:click={() => selectAll()} checked={allSelected}>
                </td>

                {#each headers as titles}

                    {#if titles === "Name"}
                    <th scope="col" class="px-6 py-3 text-left mx-0">
                        {titles}
                    </th>
                    {:else}
                    <th scope="col" class="px-6 py-3 text-right mx-0">
                        {titles}
                    </th>
                    {/if}

                {/each}
            </tr>

        </thead>

            {#key refresh}

            <tbody class="bg-gray-800 overflow-y-auto grow font-normal scrollbar rounded-b-lg">

                {#each inventoryData as card_data, i}
                    <tr class="not-last:border-b-2 border-gray-700 w-full table table-fixed">

                        <td class="px-6 py-3 text-left mx-0 w-4">
                            <input type="checkbox" class=" text-blue-600 rounded bg-gray-700 " bind:group={selected} value={card_data}>
                        </td>

                        {#each headers as data_type}
                            {#if data_type === "Name"}
                                <th scope="row" class="px-6 py-3 text-gray-900 dark:text-white text-left whitespace-preline cursor-pointer hover:text-blue-400 transition-colors" >
                                    <a href="/card/{card_data._set_short}/{card_data["Collector No."]}" use:link>
                                        {card_data["Name"]}
                                    </a>
                                    <!-- on:click={() => push(`/card/${card_data._set_short}/${card_data["Collector No."]}`)} -->
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
            {/key}

            {#if selected.length > 0}
                <tbody class="bg-white text-gray-200 dark:bg-gray-900 overflow-y-auto font-normal scrollbar rounded-b-lg h-[7%] place-items-end" transition:fly="{{duration: 400}}">
                    <button class="preordain-button delete h-full" on:click={() => {modifyInventory(selected, "/inventory/delete/?access=testing","POST"); restart()}}>Delete {selected.length}</button>
                </tbody>
            {/if}



    </table>

</div>
