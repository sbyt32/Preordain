<script lang="ts">
    import {processPriceData, type queryCard} from './data_processing';
    import {database, fetchImageFromDatabase} from "../../lib/connection"
    import PlotPriceGraph from '../../lib/components/PlotPriceGraph.svelte';
    export let params: queryCard

</script>

<div class="m-8">
    <span class="inline-block border w-full p-4">
        {#await fetchImageFromDatabase("c9f8b8fb-1cd8-450e-a1fe-892e7a323479") then cardImg}
            <img src="{cardImg}" alt="" class="h-96 inline-block align-top">
        {/await}
        {#await processPriceData({set: "vow", id: "38"}) then priceData}
            <PlotPriceGraph {priceData}/>
        {/await}

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
        {#await database(`price/${params.set}/${params.id}?days=30`) then data}
            {#each data as card}
            <tr>
                <td>{card.date}</td>
                {#each Object.values(card.prices) as priceType}
                    <td>{priceType}</td>
                {/each}
            </tr>
            {/each}
        {/await}

        </tbody>
    </table>

</div>
<!-- <style>
    p {
        width:auto;
    }
</style> -->
