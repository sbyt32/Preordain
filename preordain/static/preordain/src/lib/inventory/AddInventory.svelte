<script context="module" lang="ts">

    export const conditions = [
        { abbrev: "NM", full:"Near Mint"},
        { abbrev: "LP", full: "Lightly Played"},
        { abbrev: "MP", full: "Moderately Played"},
        { abbrev: "HP", full: "Heavily Played"},
        { abbrev: "DMG", full: "Damaged"}
    ]
    export const variants = [
        {abbrev: "Normal", full: "Non-Foil"},
        {abbrev: "Foil", full: "Foil 🌟"},
        {abbrev: "Etched", full: "Etched"},
    ]

</script>

<script lang="ts">
    import { connectURL, parseCurrency } from "../../assets/stores";
    import { database } from "../../util/fetch_data";
    import type { InventoryBody, SingleCardResponse } from "./interfaces";
    export let col_span = 4;
    export let row_span = 1

    let headers = ["USD","USD (Foil)","Euro","Euro (Foil)","TIX"]
    let price_values = ["usd","usd_foil","euro","euro_foil", "tix"]



    let cardData: SingleCardResponse

    function parseDate(currentDate: Date = new Date(Date.now())) {

        let currentMonth = currentDate.getMonth() + 1
        return `${currentDate.getFullYear()}-${currentMonth >= 10 ? currentMonth : `0${currentMonth}`}-${currentDate.getDate()}`
    }

    $: inventoryData = {
        add_date: parseDate(),
        uri: "",
        qty: null,
        buy_price: null,
        card_condition: conditions[0].abbrev,
        card_variant: variants[0].abbrev
    }

    $: params = {
        set: "",
        collector_number: ""
    }

    async function searchCard() {
        cardData = await database(`${$connectURL}/card/${params.set}/${params.collector_number}`)
        inventoryData.uri = cardData.data.uri
    }

    async function addCardInventory(data:InventoryBody) {
        if (Object.values(inventoryData).some(x => x === null || x === '')) {
            throw new Error("missing data");
        }

        await fetch(`${$connectURL}/inventory/add/?access=testing`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(data)
        }).then((data) => {
            if (data.status == 201) {
                return true
            }
            return false
            }
        )}
</script>


<div class="component-theme inline-flex" style="grid-column: span {col_span} / span {col_span}; grid-row: span {row_span} / span {row_span};">
    <div class="flex flex-col w-1/2">
        <div class="container p-2 flex flex-row w-full grow ">
            <div class="grid grid-cols-5 row-span-3 w-full gap-2">

                <input type="text" placeholder="Set Code" class="p-2 h-min col-span-2 row-span-1" bind:value={params.set}>
                <input type="text" placeholder="Collector Number" class="p-2 h-min col-span-2 row-span-1" bind:value={params.collector_number}>
                <button class="preordain-button p-2 h-min col-span-1" disabled="{!params.collector_number || !params.set}" on:click={() => searchCard()}>Search</button>


                <input type="number" placeholder="Quantity" class="p-2 h-min col-span-1 row-start-2 tabular-nums" bind:value={inventoryData.qty}>
                <input type="number" placeholder="Cost" class="p-2 h-min col-span-1 row-start-2 tabular-nums" bind:value={inventoryData.buy_price}>


                <select class="p-2 h-min col-span-2 row-start-3" bind:value={inventoryData.card_condition}>
                    {#each conditions as condition}
                        <option value="{condition.abbrev}">{condition.full}</option>
                    {/each}
                </select>
                <select class="p-2 h-min col-span-2 row-start-3 col-start-3" bind:value={inventoryData.card_variant}>
                    {#each variants as variant}
                        <option value="{variant.abbrev}">{variant.full}</option>
                    {/each}
                </select>
                <input
                    type="date"
                    class="p-2 h-min col-span-2 row-start-2 cursor-pointer"
                    min="2022-12-30"
                    max={parseDate()}
                    bind:value={inventoryData.add_date}
                >

                <button on:click={() => addCardInventory(inventoryData)} class="preordain-button p-2 h-min col-span-1 row-start-2 col-start-5" disabled="{Object.values(inventoryData).some(x => x === null || x === '')}">Add</button>

            </div>
        </div>
    </div>


    <div class="container flex flex-col">
        <div class="flex flex-col text-center content-center text-gray-200 grow">
            {#if cardData}
            <p class="font-semibold">{cardData.data.name}</p>
            <p class="font-semibold">{cardData.data.set_full} <i class="ss text-2xl ss-{cardData.data.set}"></i></p>
            {:else}
            <p class="font-semibold">Card Name</p>
            <p class="font-semibold">Set</p>
            {/if}
        </div>
        <div class="inline-flex flex-row place-content-evenly w-full pb-4">
            {#if cardData}
                {#each price_values as price, i}
                <div class="gap-1.5 inline-flex flex-col text-center flex-none">
                    <p class="border-b mx-12">{headers[i]}</p>
                    <p class="tabular-nums">{parseCurrency(cardData.data.prices[price], price)}</p>


                    <!-- <button class="preordain-button shop-tcg w-fit h-min py-1 mt-2 text-base">
                        <a target="_blank" rel="noreferrer" href="https://www.tcgplayer.com/product/">
                        To TCGPlayer 🔮
                        </a>
                    </button> -->

                </div>

                {/each}
                {:else}
                    {#each price_values as price, i}
                        <div class="gap-1.5 inline-flex flex-col text-center flex-none">
                            <p class="border-b mx-12">{headers[i]}</p>
                            <p class="tabular-nums text-gray-600/80 italic">$0.00</p>


                            <!-- <button class="preordain-button shop-tcg w-fit h-min py-1 mt-2 text-base">
                                <a target="_blank" rel="noreferrer" href="https://www.tcgplayer.com/product/">
                                To TCGPlayer 🔮
                                </a>
                            </button> -->

                        </div>
                    {/each}
            {/if}
        </div>
    </div>
</div>
