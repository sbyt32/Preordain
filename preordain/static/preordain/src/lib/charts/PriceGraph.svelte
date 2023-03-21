<script lang="ts">
    // @ts-nocheck
    import { Line } from "svelte-chartjs"
    import {parsePriceData} from "./data"
    import 'chart.js/auto';
    import { database } from "../../util/fetch_data";
    import { CurrentCard } from "../../assets/stores";
    export let col_span:number | string = 3
    export let row_span:number | string = 2

    $: options = {
        responsive: true,
        color: "#ffffff",
        plugins: {
            tooltip: {
                callbacks: {
                    label: function(context) {
                        let label = context.dataset.label || '';

                        if (label){
                            label += ': ';
                        }
                        if (context.datasetIndex == 0 || context.datasetIndex == 1) {
                            label += new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(context.parsed.y);
                        } else if (context.datasetIndex == 2 || context.datasetIndex == 3) {
                            label += new Intl.NumberFormat('de-DE', { style: 'currency', currency: 'EUR' }).format(context.parsed.y);
                        } else {
                            label += `${context.parsed.y} TIX`
                        }
                        return label;
                    }
                },
                intersect: false
            },
            title: {
                display: true,
                text: `Price History for ${$CurrentCard.card}`,
                color: `#ffffff`
            },
            legend: {
                display: true,
                position: "top"
            }
        },
        interaction: {
            mode: 'index'
        },
        scales: {
            x: {
                title: {
                    display: true,
                    text: 'Date'
                }
            },
            y: {
                title: {
                    display: true,
                    text: 'Price'
                }
            }
        }
    }

    const connectURL = import.meta.env.VITE_CONNECTION;
    $: db_data = database(`${connectURL}/price/${$CurrentCard.set_name}/${$CurrentCard.id}?max=31`)
</script>

{#key CurrentCard}
    {#await db_data then data}
        <div style="grid-column: span {col_span} / span {col_span}; grid-row: span {row_span} / span {row_span};" class="shadow-2xl component-theme min-h-0">
            <Line
            data={parsePriceData(data)}
            options={options}
            />
        </div>
    {/await}
{/key}
