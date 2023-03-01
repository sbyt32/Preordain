<script lang="ts" context="module">
    export let headers = ["USD","USD (Foil)","Euro","Euro (Foil)","TIX"]
    export let price_values = ["usd","usd_foil","euro","euro_foil", "tix"]
</script>

<script lang="ts">
    import { parseCurrency, CurrentCard } from "../assets/functions"
    import { database } from "../fetch_data";

    $: updateData = database(`http://127.0.0.1:8000/api/price/${$CurrentCard.set_name}/${$CurrentCard.id}?max=1`)

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

        <div class="component-theme shadow-lg">
            <div class="inline-grid grid-rows-4 grid-cols-6 ">

                <img class="col-span-1 row-span-4 h-64 w-full md:overflow-hidden rounded-2xl bg-inherit p-2"
                src="./img/{prices.data.set}_{prices.data.id}.jpg"
                alt="{prices.data.name} from {prices.data.set_full}">
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
                <div class="text-center">
                    <button class="component-theme w-fit px-3 py-1 text-base">
                        To Scryfall 🔮
                    </button>
                </div>

            </div>
        </div>

    {/await}
{/key}
