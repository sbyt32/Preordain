<script lang="ts">
    // @ts-nocheck
    import { Line } from "svelte-chartjs"
    import { data } from "./test_data";
    import 'chart.js/auto';
    export const options = {
        maintainAspectRatio: false,
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
                text: 'Price History'
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
</script>

<div class="component-theme text-white shadow-lg h-full w-full">
        <Line
        data={data}
        options={options}
        />
</div>
