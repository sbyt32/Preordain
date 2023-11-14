<script lang="ts">
    import type { PageServerData } from './$types';
    import PlotPriceGraph from "$lib/components/PlotPriceGraph.svelte";
    import CardMetadataDisplayer from '$lib/components/CardMetadataDisplayer.svelte';

    export let data: PageServerData

    function parseHeaders(headers:Array<String>) {
        let new_headers:Array<String> = []
        headers.forEach(header => {
            header = header.replace("_", " ")
                    .replace("foil", "(Foil)")
                    .replace("etch", "(Etched)")
                    .replace("euro", "Euro")
                    .replace("tix", "Tix")
                    .replace("usd", "USD")

            new_headers.push(header)
        });
        return new_headers
    }

</script>

<div class="m-8">

        <!-- <img src="{data.image}" alt=""> -->
    <CardMetadataDisplayer imgURL={data.image} cardData={data.card}/>

    <div>
        <PlotPriceGraph data={data.price}/>
    </div>

    <table class="table-auto w-full">
        <thead>
            <tr>
                {#each parseHeaders(Object.keys(data.price[0].prices)) as header}
                    <th class="">{header}</th>
                {/each}
            </tr>
        </thead>
        <tbody>
        {#each data.price as card}
            <tr>
                <td>{card.date}</td>
                {#each Object.values(card.prices) as priceType}
                    <td>{priceType == null ? "" : priceType}</td>
                {/each}
            </tr>
        {/each}
        </tbody>
    </table>

</div>
