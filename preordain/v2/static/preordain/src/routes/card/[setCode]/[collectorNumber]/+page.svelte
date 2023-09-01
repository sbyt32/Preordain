<script lang="ts">
    import type { PageData } from './$types';
    import * as Plot from '@observablehq/plot'
    export let data: PageData

    let div: HTMLDivElement;

    // let usd = true
    interface chartPrice {
            Date: Date
            Type: string
            Currency: string
            Price: string | number | null
    }
    let priceData:chartPrice[] = []
    data.price.forEach(e => {
        priceData.push(
            { "Date": new Date(e.date), "Type": "USD", "Currency": "USD", "Price":  e.prices.usd },

            { "Date": new Date(e.date), "Type": "USD (Foil)", "Currency": "USD", "Price": (e.prices.usd_foil != null ? e.prices.usd_foil : null) },
            { "Date": new Date(e.date), "Type": "USD (Etched)", "Currency": "USD", "Price": e.prices.usd_etch },
            // { "Date": new Date(e.date), "Type": "Euro", "Price": e.prices.euro },
            // { "Date": new Date(e.date), "Type": "Euro (Foil)", "Price": e.prices.euro_foil },
            // { "Date": new Date(e.date), "Type": "Tickets", "Price": (e.prices.tix != null ? e.prices.tix.toLocaleString("en-US", {style: "currency", currency: "USD"}) : null)},
        )
    });

    const chartData = Plot.plot({
        height: 396,
        width: (window.screenX * .9),
        margin: 28,
        color: {legend: true},
        marks: [
            Plot.frame(),
            // Plot.ruleY([0]),
            Plot.lineY(priceData, {x: "Date", y: "Price", stroke: "Type", sort: {y: "y"}}),
            Plot.crosshair(priceData, {x: "Date", y: "Price"}),
            Plot.tip(priceData, Plot.pointer(
                {x: 'Date', y: "Price", channels: {currency: "Currency", }}
            ))
        ]
    })

    $: {
        div?.firstChild?.remove(); // remove old chart, if any
        div?.append(chartData); // add the new chart
  }

</script>

<div class="m-8">
    <div bind:this={div} role="img" class="pb-8"></div>

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
