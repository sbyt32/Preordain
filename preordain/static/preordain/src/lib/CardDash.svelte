<script lang="ts" context="module">
    export let headers = ["USD","USD (Foil)","Euro","Euro (Foil)","TIX"]
    export let price_values = ["usd","usd_foil","euro","euro_foil", "tix"]
</script>
<script lang="ts">
    const connectURL = import.meta.env.VITE_CONNECTION;
    import { CurrentCard } from "../assets/stores"
    import { parsePercentage, parseCurrency } from "../util/dataFormatter"

    export let col_span:number = 3
    export let row_span:number = 1


    // $: updateData = database(`/price/${$CurrentCard.set_name}/${$CurrentCard.id}?max=1`)
    // $: buyButtons = database(`${connectURL}/card/buylinks/${$CurrentCard.set_name}/${$CurrentCard.id}`)
    async function getImage(set:string, id:string) {
        const cardImg = await fetch(`${connectURL}/card/images/${set}/${id}/`)
        return URL.createObjectURL(await cardImg.blob())
    }
    $: cardImage = getImage($CurrentCard.set_name, $CurrentCard.id)

</script>


        <div style="grid-column: span {col_span} / span {col_span}; grid-row: span {row_span} / span {row_span};" class="shadow-2xl component-theme min-h-0 w-full">


            <div class="flex flex-row w-full h-full p-4" style="{col_span >= 3? 'grid-template-columns: repeat(6, minmax(0, 1fr));': 'grid-template-columns: repeat(5, minmax(0, 1fr));'}">
                {#key CurrentCard}

                {#if col_span >=3}
                    {#await cardImage then image}
                    <div class="h-full">
                        <img class="md:overflow-hidden object-contain rounded-2xl bg-inherit place-self-start h-full"
                        src="{image}"
                        alt="{$CurrentCard.card} from {$CurrentCard.set_name}">
                    </div>
                    {/await}
                {/if}


                <div class="text-center text-gray-200 text-lg content-end flex flex-col grow">

                    <!-- Text Header -->
                    <div class="flex flex-col text-center content-center text-gray-200 grow">
                        <p class="font-semibold">{$CurrentCard.card} <span class="font-normal text-base">{$CurrentCard.set_name} <i class="ss text-2xl ss-{$CurrentCard.set_name}"></i></span></p>
                    </div>

                    <!-- Price Body -->
                    <div class="flex flex-row place-content-evenly">
                        {#each price_values as price, i}
                            <div class="gap-1.5 inline-flex flex-col">
                                <p class="border-b mx-8">{headers[i]}</p>

                                <p style="font-variant-numeric: tabular-nums">
                                    {parseCurrency($CurrentCard.prices[price], price)}
                                </p>

                                <!-- {@html parsePercentage($CurrentCard.prices[0][`${price}_change`])} -->

                                <button class="preordain-button shop-tcg w-fit px-3 py-1 mt-2 mx-auto text-base">
                                    <a target="_blank" rel="noreferrer" href="https://www.tcgplayer.com/product/">
                                    To TCGPlayer 🔮
                                    </a>
                                </button>

                            </div>
                        {/each}
                    </div>

                </div>


                {/key}
            </div>
        </div>

<!-- https://www.cardmarket.com/en/Magic/Products/Search?searchString={prices.data.name.toLowerCase()} -->
<!-- https://www.cardhoarder.com/cards?data%5Bsearch%5D={prices.data.name.toLowerCase()} -->
