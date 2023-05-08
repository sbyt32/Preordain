<script lang="ts">
    // @ts-nocheck
    import { Line } from "svelte-chartjs"
    import {parsePriceData} from "./data"
    import 'chart.js/auto';
    import { database } from "../../util/fetch_data";
    export let set: string
    export let id: string
    export let cardName: string


    const options = {
        responsive: true,
        maintainAspectRatio: false,
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
                text: `Price History for ${cardName}`,
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

</script>

    {#await database(`/price/${set}/${id}?max=31`) then data}
            <Line
            data={parsePriceData(data)}
            options={options}
            />
    {/await}
