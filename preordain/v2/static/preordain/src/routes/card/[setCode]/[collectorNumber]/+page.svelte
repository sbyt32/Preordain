<script lang="ts">
    import type { PageData } from './$types';
    import * as Plot from '@observablehq/plot'
    export let data: PageData

    let div: HTMLDivElement;

    let usd = true
    interface chartPrice {
            Date: Date
            Type: string
            Price: string | number
    }
    let priceData:chartPrice[] = []
    data.price.forEach(e => {
        priceData.push(
            { "Date": new Date(e.date), "Type": "USD", "Price": e.prices.usd.toLocaleString("en-US", {style: "currency", currency: "USD"})  },
            { "Date": new Date(e.date), "Type": "USD (Foil)", "Price": e.prices.usd_foil.toLocaleString("en-US", {style: "currency", currency: "USD"}) },
            // { "Date": new Date(e.date), "Type": "USD (Etched)", "Price": e.prices.usd_etch.toLocaleString("en-US", {style: "currency", currency: "USD"}) },
            // { "Date": new Date(e.date), "Type": "Euro", "Price": e.prices.euro },
            // { "Date": new Date(e.date), "Type": "Euro (Foil)", "Price": e.prices.euro_foil },
            { "Date": new Date(e.date), "Type": "Tickets", "Price": e.prices.tix.toLocaleString("en-US", {style: "currency", currency: "USD"})},
        )
    });

    const chartData = Plot.plot({
        color: {legend: true},
        marks: [
            Plot.frame(),
            Plot.lineY(priceData, {x: "Date", y: "Price", stroke: "Type", sort: {y: "y"}}),
            Plot.crosshair(priceData, {x: "Date", y: "Price"}),
            Plot.tip(priceData, Plot.pointer(
                {x: 'Date', y: "Price", anchor: "top-right"}
            )
            )
        ]
    })

    $: {
        div?.firstChild?.remove(); // remove old chart, if any
        div?.append(chartData); // add the new chart
  }

</script>

<div bind:this={div} role="img"></div>

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
