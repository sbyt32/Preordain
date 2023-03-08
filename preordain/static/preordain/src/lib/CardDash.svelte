<script lang="ts" context="module">
    export let headers = ["USD","USD (Foil)","Euro","Euro (Foil)","TIX"]
    export let price_values = ["usd","usd_foil","euro","euro_foil", "tix"]
</script>

<script lang="ts">
    import { parseCurrency, CurrentCard } from "../assets/functions"
    import { database } from "../fetch_data";
    export let col_span:number | string = 3

    $: updateData = database(`http://127.0.0.1:8000/api/price/${$CurrentCard.set_name}/${$CurrentCard.id}?max=1`)
    $: buyButtons = database(`http://127.0.0.1:8000/api/card/buylinks/${$CurrentCard.set_name}/${$CurrentCard.id}`)

    function parsePercentage(percent:string) {
        if (percent == null) {
            return ""
        }
        let change = parseFloat(percent)
        let classes = "text-black"
        let emoji = " "
        if (change > 0) {
            emoji = "📈 "
            classes = "text-emerald-500"
        } else if (change < 0) {
            emoji = "📉 "
            classes = "text-rose-500"
        }
        return `<p class=${classes}>${emoji}${percent}</p>`
    }

</script>
{#key CurrentCard}
    {#await updateData then prices}
    <span style="grid-column: span {col_span} / span {col_span}" class="shadow-2xl">
        <div class="component-theme shadow-lg h-full">
            <div class="inline-grid grid-rows-4 grid-cols-6 w-full" style="{col_span >= 3? 'grid-template-columns: repeat(6, minmax(0, 1fr));': 'grid-template-columns: repeat(5, minmax(0, 1fr));'}">
                {#if col_span>=3}
                <img class="col-span-1 row-span-4 w-full md:overflow-hidden rounded-2xl bg-inherit p-2 place-self-center"
                src="./img/{prices.data.set}_{prices.data.id}.jpg"
                alt="{prices.data.name} from {prices.data.set_full}">
                {/if}

                <div class="col-span-5 text-center text-white">
                    <span>
                        <p>{prices.data.name}</p>
                        <p>{prices.data.set_full} <i class="ss text-2xl ss-{prices.data.set}"></i></p>
                    </span>
                </div>

                {#each headers as header}
                    <div class="col-span-1 text-center text-white">
                        <span class="col-span-1">{header}</span>
                    </div>
                {/each}

                {#each price_values as price}
                    <div class="col-span-1 text-center text-white text-lg">
                        <p>
                            {parseCurrency(prices.data.prices[0][price], price)}
                        </p>
                        {@html parsePercentage(parsePercentage(prices.data.prices[0][`${price}_change`]))}
                    </div>
                {/each}
                <!-- Button Placeholder -->
                <div class="col-span-5 inline-grid grid-cols-5 content-center text-center">
                    {#await buyButtons then buttons}
                        <a class="component-theme w-fit px-3 py-1 mx-auto text-base" href="https://www.tcgplayer.com/product/{buttons.data.tcg_id}">
                            To TCGPlayer 🔮
                        </a>
                        <a class="component-theme w-fit px-3 py-1 mx-auto text-base" href="https://www.tcgplayer.com/product/{buttons.data.tcg_id}">
                            To TCGPlayer 🔮
                        </a>
                        <a class="component-theme w-fit px-3 py-1 mx-auto text-base" href="https://www.tcgplayer.com/product/{buttons.data.tcg_id}">
                            To CardMarket 🫘
                        </a>
                        <a class="component-theme w-fit px-3 py-1 mx-auto text-base" href="https://www.tcgplayer.com/product/{buttons.data.tcg_id}">
                            To CardMarket 🫘
                        </a>
                        <a class="component-theme w-fit px-3 py-1 mx-auto text-base" href="https://www.tcgplayer.com/product/{buttons.data.tcg_id}">
                            To CardHoarder 🤖
                        </a>
                    {/await}
                </div>
            </div>
        </div>
    </span>
    {/await}
{/key}
