<script lang="ts" context="module">
    export let headers = ["USD","USD (Foil)","Euro","Euro (Foil)","TIX"]
    export let price_values = ["usd","usd_foil","euro","euro_foil", "tix"]
</script>
<script lang="ts">
    const connectURL = import.meta.env.VITE_CONNECTION;
    import { parseCurrency, CurrentCard } from "../assets/stores"
    import { parsePercentage } from "../util/parseValues"
    import { database } from "../util/fetch_data";

    export let col_span:number | string = 3
    export let row_span:number | string = 1


    $: updateData = database(`${connectURL}/price/${$CurrentCard.set_name}/${$CurrentCard.id}?max=1`)
    $: buyButtons = database(`${connectURL}/card/buylinks/${$CurrentCard.set_name}/${$CurrentCard.id}`)

</script>
{#key CurrentCard}
    {#await updateData then prices}
    <div style="grid-column: span {col_span} / span {col_span}; grid-row: span {row_span} / span {row_span};" class="shadow-2xl">
        <div class="component-theme shadow-lg h-full">
            <div class="inline-grid grid-rows-4 grid-cols-6 w-full" style="{col_span >= 3? 'grid-template-columns: repeat(6, minmax(0, 1fr));': 'grid-template-columns: repeat(5, minmax(0, 1fr));'}">
                {#if col_span>=3}
                <img class="col-span-1 row-span-4 w-full md:overflow-hidden rounded-2xl bg-inherit p-2 place-self-center"
                src="./img/{prices.data.set}_{prices.data.id}.jpg"
                alt="{prices.data.name} from {prices.data.set_full}">
                {/if}

                <div class="col-span-5 text-center text-gray-200">
                    <span>
                        <p class="font-semibold">{prices.data.name}</p>
                        <p>{prices.data.set_full} <i class="ss text-2xl ss-{prices.data.set}"></i></p>
                    </span>
                </div>

                {#each headers as header}
                    <div class="col-span-1 text-center text-gray-200">
                        <span class="col-span-1">{header}</span>
                    </div>
                {/each}

                {#each price_values as price}
                    <div class="col-span-1 text-center text-gray-200 text-lg">
                        <p style="font-variant-numeric: tabular-nums">
                            {parseCurrency(prices.data.prices[0][price], price)}
                        </p>
                        {@html parsePercentage(prices.data.prices[0][`${price}_change`])}
                    </div>
                {/each}
                <!-- Button Placeholder -->
                <div class="col-span-5 inline-grid grid-cols-5 content-center text-center">
                    {#await buyButtons then buttons}
                        <a class="component-theme w-fit px-3 py-1 mx-auto text-base hover:bg-[#4D7C0F] transition-colors" target="_blank" rel="noreferrer" href="https://www.tcgplayer.com/product/{buttons.data.tcg_id}">
                            To TCGPlayer 🔮
                        </a>
                        <a class="component-theme w-fit px-3 py-1 mx-auto text-base hover:bg-[#4D7C0F] transition-colors" target="_blank" rel="noreferrer" href="https://www.tcgplayer.com/product/{buttons.data.tcg_id}">
                            To TCGPlayer 🔮
                        </a>
                        <a class="component-theme w-fit px-3 py-1 mx-auto text-base hover:bg-[#185C9E] transition-colors" target="_blank" rel="noreferrer" href="https://www.cardmarket.com/en/Magic/Products/Search?searchString={prices.data.name.toLowerCase()}">
                            To CardMarket 🫘
                        </a>
                        <a class="component-theme w-fit px-3 py-1 mx-auto text-base hover:bg-[#185C9E] transition-colors" target="_blank" rel="noreferrer" href="https://www.cardmarket.com/en/Magic/Products/Search?searchString={prices.data.name.toLowerCase()}">
                            To CardMarket 🫘
                        </a>
                        <a class="component-theme w-fit px-3 py-1 mx-auto text-base hover:bg-[#EA580C] transition-colors" target="_blank" rel="noreferrer" href="https://www.cardhoarder.com/cards?data%5Bsearch%5D={prices.data.name.toLowerCase()}">
                            To CardHoarder 🤖
                        </a>
                    {/await}
                </div>
            </div>
        </div>
    </div>
    {/await}
{/key}
