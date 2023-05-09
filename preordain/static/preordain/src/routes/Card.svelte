<script lang="ts">
  import PriceButtons from '../lib/card/PriceButtons.svelte';

    import OtherVariants from '../lib/card/OtherVariants.svelte';
    import PriceGraph from "../lib/charts/PriceGraph.svelte";

    import { database } from "../util/fetch_data";
    import { connectURL } from "../assets/stores";
    import { parseOracleText, parseFormatLegality} from "../util/dataFormatter";
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
        <div class="flex flex-row gap-4">
            <div class="component-theme">

                <div class="m-4 content-center">
                    <div class="flex flex-col w-full text-center">
                        <p class="text-lg font-semibold">{data.data.name}</p>
                        <p class="font-normal italic text-base">{data.data.set_full} <i class="ss ss-{data.data.set} ss-{data.data.rarity} text-2xl"/></p>
                    </div>

                    <div class="inline-flex flex-row">
                        {#await getImage() then imgURL}
                            <div class="w-1/3 bottom-0 mr-4 my-auto">
                                <img class=" h-fit border object-scale-down rounded-xl "
                                src="{imgURL}" alt={data.data.name}>

                                <PriceButtons {params} name={data.data.name}/>

                            </div>
                        {/await}

                        <div class="inline-flex flex-col align-center text-center grow w-full gap-2">
                            <div class="container mx-auto component-theme px-4 py-1 leading-loose grow flex flex-col">
                                <div class="text-right"><span class="font-semibold">Mana Cost: </span>{data.data.mana_cost}</div>
                                <div class="text-left"><span class="font-semibold">Type:</span> Legendary Creature - Human Soldier</div>
                                {@html parseOracleText(data.data.oracle_text)}
                                <div class="text-left"><span class="font-semibold">Artist: </span>{data.data.artist}</div>
                            </div>

                            <div class="container mx-auto component-theme px-4 py-1">
                                <p class="font-semibold border-b mx-auto w-2/4">Legality</p>
                                <div class="grid grid-cols-4 gap-3 py-2">
                                    {#each Object.keys(data.data.legality) as format}
                                            <span class="font-semibold text-left px-4">
                                                {format[0].toUpperCase()+format.slice(1)} <!-- Very hacky way of doing "Capitalize the first character"-->
                                            </span>
                                            {@html parseFormatLegality(data.data.legality[format])}
                                    {/each}
                                </div>
                            </div>
                        </div>
                    </div>

                </div>

            </div>

            <OtherVariants {params}/>

        </div>


        <div class="flex flex-row gap-4 grow">
            <div class="h-full grow component-theme">
                <PriceGraph set={params.set} id={params.cn} cardName={data.data.name}/>
            </div>
        </div>

    </div>

    {/await}
{/if}
