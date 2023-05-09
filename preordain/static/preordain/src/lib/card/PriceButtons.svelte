<script lang="ts">
    import OtherVariants from './OtherVariants.svelte';
    import PriceGraph from "../charts/PriceGraph.svelte";

    import { database } from "../../util/fetch_data";
    export let params = null
    export let name: string


</script>



<div class="flex flex-col">
    <div class="inline-flex gap-4 text-base mt-2">

        {#await database(`/card/buylinks/${params.set}/${params.cn}`)}
            <button class="preordain-button shop-tcg w-full group" disabled>
                <a target="_blank" rel="noreferrer" class="group-hover:underline"
                href="https://www.tcgplayer.com/product">
                Loading...
                </a>
            </button>
            <button class="preordain-button shop-tcg w-full group" disabled>
                <a target="_blank" rel="noreferrer" class="group-hover:underline"
                href="https://www.tcgplayer.com/product/">
                Loading...
                </a>
            </button>
        {:then tcgLink}
            <button class="preordain-button shop-tcg w-full group">
                <a target="_blank" rel="noreferrer" class="group-hover:underline"
                href="https://www.tcgplayer.com/product/{tcgLink.data.tcg_id}">
                TCG
                </a>
            </button>
            <button class="preordain-button shop-tcg w-full group">
                <a target="_blank" rel="noreferrer" class="group-hover:underline"
                href="https://www.tcgplayer.com/product/{tcgLink.data.tcg_id}?Printing=Foil">
                TCG 🌟
                </a>
            </button>
        {/await}

    </div>

    <button class="preordain-button shop-mkm mt-2 w-full group text-base">
        <a target="_blank" rel="noreferrer" class="group-hover:underline"
        href="https://www.cardmarket.com/en/Magic/Products/Search?searchString={name}">
        MKM
        </a>
    </button>

    <button class="preordain-button shop-ch mt-2 w-full text-base">
        <a target="_blank" rel="noreferrer" href="https://www.cardhoarder.com/cards?data%5Bsearch%5D={name.toLowerCase()}">
        Cardhoarder
        </a>
    </button>

</div>
