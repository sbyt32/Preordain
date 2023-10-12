<script lang="ts">
    // IDK why this is giving an error
    // @ts-ignore
    import * as d3 from "d3"
    import * as Plot from '@observablehq/plot'
    let div: HTMLSpanElement;
    export let priceData;


    const chartData = Plot.plot({
        height: window.screenY,
        width: window.screenX * .58,
        // margin: 32,

        color: {legend: true},
        style: "overflow: visible; font-size: 13px;",
        y: {grid: true, label: "Price", tickFormat: d3.format("$,.2f") },
        marks: [
            Plot.ruleY([0]),
            Plot.axisX({ticks:"week"}),
            Plot.gridX({ticks: "month", strokeWidth: 2, stroke: "blue", strokeOpacity: .2}),
            Plot.lineY(priceData, {x: "Date", y: "Price", stroke: "Type", strokeWidth: 2}),
            // Plot.text(priceData, Plot.selectFirst({x: "Date", y: "Price", z: "Type", text: "Type", textAnchor:"start", dx: 3})),

            Plot.crosshair(priceData, {x: "Date", y: "Price"}),
            Plot.tip(priceData, Plot.pointerX(
                {x: 'Date', y: "Price", channels: {Date: "Date", Currency: "Currency", Price: "Price" }}
            ))
        ]
    })

    $: {
        div?.firstChild?.remove(); // remove old chart, if any
        div?.append(chartData); // add the new chart
  }

</script>

<span bind:this={div} role="img" class="inline-block align-top w-fit"/>
