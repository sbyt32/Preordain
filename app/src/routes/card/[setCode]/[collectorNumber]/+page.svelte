<script lang="ts">
    import type { PageServerData } from './$types';
    import PlotPriceGraph from "$lib/components/PlotPriceGraph.svelte";
    export let data: PageServerData

    let div: HTMLDivElement;

    const headers = Object.keys(data.price[0].prices)


</script>

<div class="m-8">


    <PlotPriceGraph data={data.price}/>

    <table class="table-auto w-full">
        <thead>
            <tr>
                {#each headers as header}
                    <th class="uppercase">{header}</th>
                {/each}
                <!-- <th>Date</th>
                <th>USD</th>
                <th>USD (Foil)</th>
                <th>USD (Etched)</th>
                <th>Euro</th>
                <th>Euro (Foil)</th>
                <th>TIX</th> -->
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
