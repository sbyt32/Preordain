<script lang="ts">
    import type { PageData } from './$types';
    import PlotPriceGraph from "$lib/components/PlotPriceGraph.svelte";
    export let data: PageData

    let div: HTMLDivElement;

    // let usd = true



</script>

<div class="m-8">
    <PlotPriceGraph priceData={data}/>

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
        {#each data.price as card}
            <tr>
                <td>{card.date}</td>
                {#each Object.values(card.prices) as priceType}
                    <td>{priceType}</td>
                {/each}
            </tr>
        {/each}
        </tbody>
    </table>

</div>
