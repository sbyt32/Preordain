<script lang="ts" context="module">
    export let headers = ["USD","USD (Foil)","Euro","Euro (Foil)","TIX"]
    export let prices = ["usd","usd_foil","euro","euro_foil", "tix"]
</script>

<script lang="ts">
    import type { GetPriceSingle } from "../assets/responses";
    export let data: GetPriceSingle;

    function parsePercentage(percent:string) {
        let change = parseFloat(percent)
        if (change > 0) {
            return "text-emerald-500"
        } else if (change < 0) {
            return "text-rose-500"
        } else {
            return "text-black"
        }
    }

    function parseCurrency(price:number, currency:string) {
        if (currency.toLowerCase().includes("usd")) {
            let stuff = new Intl.NumberFormat("en-US", {style: 'currency', currency: 'USD'}).format(price)
            return stuff
        } else if (currency.toLowerCase().includes("euro")) {
            let stuff = new Intl.NumberFormat("de-DE", {style: 'currency', currency: 'EUR'}).format(price)
            return stuff
        } else {
            return `${price} TIX`
        }
    }
</script>

<div class="flex flex-col bg-white border border-gray-200 rounded-lg shadow md:flex-row hover:bg-gray-100 dark:border-gray-700 dark:bg-gray-800 dark:hover:bg-gray-700">
    <img class="object-cover rounded-t-lg h-96 md:h-auto md:w-48 md:rounded-xl md:rounded-l-lg" src="./img/{data.data.set}_{data.data.id}.jpg" alt="">
    <div class="grid grid-rows-4 grid-cols-5 text-center w-full text-white">
        <div class="col-span-5 self-auto max-h-fit">
            <p> {data.data.name} </p>
            <p> {data.data.set_full} </p>
        </div>
        {#each headers as header}
        <div>
            <p>
                {header}
            </p>
        </div>
        {/each}
        {#each prices as price}
            <div>
                <p>
                    {parseCurrency(data.data.prices[0][price], price)}
                </p>
                <p class={parsePercentage(data.data.prices[0][`${price}_change`])}>
                    {data.data.prices[0][`${price}_change`]}
                </p>
            </div>
        {/each}
    </div>
</div>
