<script lang="ts">
    // IDK why this is giving an error
    // @ts-ignore
    import * as d3 from "d3"
    import * as Plot from '@observablehq/plot'
    import type { PriceResponse } from "$lib/responses";
    let div: HTMLSpanElement;
    export let data:PriceResponse[];

    interface ChartPrice {
        Date: Date
        Type: string
        Currency: string
        Price: string | number | null
    }
    let parsedChartData:ChartPrice[] = []

    data.forEach(e => {
        let currentDate = new Date(e.date)
        parsedChartData.push(
            {"Date": currentDate, "Type": "USD", "Currency": "USD", "Price": e.prices.usd},
            {"Date": currentDate, "Type": "USD", "Currency": "USD", "Price": e.prices.usd_foil}
            )
    })

    const chartVisual = Plot.plot({
        height: window.screenY,
        width: window.screenX * .58,

        // margin: 32,
        title: "Price History",
        color: {legend: true},
        style: "overflow: visible; font-size: 13px;",
        y: {grid: true, label: "Price", tickFormat: d3.format("$,.2f") },
        marks: [

            // TODO: Add BG
            // Plot.frame({fill: "#"}),
            Plot.ruleY([0]),

            Plot.axisX({ticks:"week"}), // Set X axis to break up by week
            Plot.gridX({ticks: "month", strokeWidth: 2, stroke: "blue", strokeOpacity: .2}),

            Plot.lineY(parsedChartData, {x: "Date", y: "Price", stroke: "Type", strokeWidth: 2}),
            Plot.text(parsedChartData, Plot.selectFirst({x: "Date", y: "Price", z: "Type", text: "Type", textAnchor:"start", dx: 3})),

            Plot.crosshair(parsedChartData, {x: "Date", y: "Price"}),
            Plot.tip(parsedChartData, Plot.pointerX(
                {x: 'Date', y: "Price", channels: {Date: "Date", Currency: "Currency", Price: "Price" }}
            ))
        ]
    })

    $: {
        div?.firstChild?.remove(); // remove old chart, if any
        div?.append(chartVisual); // add the new chart
    }

</script>

<div bind:this={div} role="img" class="inline-block align-top w-fit"/>
