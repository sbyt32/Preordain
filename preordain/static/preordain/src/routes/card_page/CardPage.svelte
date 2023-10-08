<script lang="ts">
    import {processPriceData, type queryCard} from './data_processing';
    import {database, fetchImageFromDatabase} from "../../lib/connection"
    import PlotPriceGraph from '../../lib/components/card_page/PlotPriceGraph.svelte';
    import CardMetadata from '../../lib/components/card_page/CardMetadata.svelte';
    export let params = null


</script>

<div class="m-8">
    <span class="inline-block border w-full p-4">
        {#await fetchImageFromDatabase("") then cardImg}
            <img src="{cardImg}" alt="" class="h-96 inline-block align-top">
        {/await}

        <!-- {#await processPriceData({set: "vow", id: "38"}) then priceData}
            <PlotPriceGraph {priceData}/>
        {/await} -->

    </span>

    <table class="table-auto w-full">
        <thead>
            <tr>
                <th>Date</th>
                <th>USD</th>
                <th>USD (Foil)</th>
                <th>USD (Etched)</th>
                <th>Euro</th>
                <th>Euro (Foil)</th>
                <th>TIX</th>
            </tr>
        </thead>
        <tbody>
        <!-- {#await database(`price/${params.set}/${params.id}?days=30`) then data}
            {#each data as card}
            <tr>
                <td>{card.date}</td>
                {#each Object.values(card.prices) as priceType}
                    <td>{priceType}</td>
                {/each}
            </tr>
            {/each}
        {/await} -->

        </tbody>
    </table>

</div>
