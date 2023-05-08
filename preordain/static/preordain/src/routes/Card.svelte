<script lang="ts">
    import { database } from "../util/fetch_data";
    import { connectURL } from "../assets/stores";
    import PriceGraph from "../lib/charts/PriceGraph.svelte";
    import { parseOracleText, parseFormatLegality, parseCurrency } from "../util/dataFormatter";
    import { link, push } from "svelte-spa-router";
    export let params = null

    async function getImage() {
        const cardImg = await fetch(`${$connectURL}/card/images/${params.set}/${params.cn}`)
        return URL.createObjectURL(await cardImg.blob())
    }


</script>
{#if params.cn && params.set}
    {#await database(`/card/metadata/${params.set}/${params.cn}`) then data}
    <div class="gap-4 flex flex-col h-full">

        <!-- Card information -->
        <div class="component-theme w-full">

            <div class="m-4 flex flex-row content-center">

                {#await getImage() then imgURL}
                <div class="w-1/5 mr-4 ">
                    <img class="h-full object-scale-down "
                    src="{imgURL}" alt={data.data.name}>

                </div>

                {/await}

                <div class="inline-flex flex-col align-center text-center grow w-full gap-2">
                    <p class="text-lg font-semibold">{data.data.name}</p>
                    <p class="font-normal italic text-base">{data.data.set_full} <i class="ss ss-{data.data.set} ss-{data.data.rarity} text-2xl"/></p>

                    <div class="container mx-auto component-theme  px-4 py-1 leading-loose">
                        <div class="text-right"><span class="font-semibold">Mana Cost: </span>{data.data.mana_cost}</div>
                        <div class="text-left"><span class="font-semibold">Type:</span> Legendary Creature - Human Soldier</div>
                        {@html parseOracleText(data.data.oracle_text)}
                        <div class="text-left"><span class="font-semibold">Artist: </span>{data.data.artist}</div>
                    </div>

                    <div class="container mx-auto component-theme px-4 leading-loose py-3">
                        Legality
                        <div class="grid grid-cols-4 gap-2">
                            {#each Object.keys(data.data.legality) as format}
                                    <span class="font-semibold text-left px-4">
                                        {format[0].toUpperCase()+format.slice(1)}
                                    </span>  <!-- Very hacky way of doing "Capitalize the first character"-->
                                    {@html parseFormatLegality(data.data.legality[format])}
                            {/each}
                        </div>
                    </div>

                </div>


            </div>
        </div>

        <div class="flex flex-row gap-4 grow">
            <div class="h-full grow component-theme">
                <PriceGraph set={params.set} id={params.cn} cardName={data.data.name}/>
            </div>



            <!-- Other Variants -->
            <div class="component-theme w-1/4 text-center pb-4">
                <span class="font-semibold">Other Variants</span>

                <table class="table-auto w-full ">

                    <thead class="border-b border-blue-500">
                        <tr>
                            <th class="text-left pl-4"><i class="ss invisible ss-fw"/> Set</th>
                            <th class="text-right pr-4">Price</th>
                        </tr>
                    </thead>

                    <tbody>
                        {#await database(`/price/variants/${params.set}/${params.cn}`)}
                            <tr>
                                <td class="text-left">Loading...</td>
                                <td class="text-right">Loading...</td>
                            </tr>
                        {:then prices}
                            {#each prices.data as price}
                            <tr>
                                <td class="text-left pl-4"><i class="ss ss-{price.set} ss-{price.rarity} ss-fw"/> <a href="/card/{price.set}/{price.id}" use:link> {price.set_full}</a></td>
                                <td class="text-right tabular-nums pr-4">{price.usd ? parseCurrency(price.usd, "usd") : price.usd_foil ? `🌟 ${parseCurrency(price.usd_foil, "usd")}` : "N/A"}</td>
                            </tr>
                            {/each}
                        {/await}
                    </tbody>

                </table>
            </div>
        </div>

    </div>

    {/await}
{/if}
