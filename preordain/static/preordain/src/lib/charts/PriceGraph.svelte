<script lang="ts">
    // @ts-nocheck
    import { Line } from "svelte-chartjs"
    import {parsePriceData} from "./data"
    import 'chart.js/auto';
    import { database } from "../../fetch_data";
    import { CurrentCard } from "../../assets/functions";
    export let col_span:number | string = 3

    $: options = {
        responsive: true,
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
                text: `Price History for ${$CurrentCard.card}`
            },
            legend: {
                display: true,
                position: "right"
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

    $: db_data = database(`http://127.0.0.1:8000/api/price/${$CurrentCard.set_name}/${$CurrentCard.id}?max=25`)
</script>

{#key CurrentCard}
    {#await db_data then data}
        <span style="grid-column: span {col_span} / span {col_span}" class="shadow-2xl w-full h-full row-span-2">
            <Line
            data={parsePriceData(data)}
            options={options}
            />
        </span>
    {/await}
{/key}
