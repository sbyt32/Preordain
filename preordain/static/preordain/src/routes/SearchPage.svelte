<script lang="ts">
    export let params;
    console.log(params);

    import {handleSubmit} from "../util/search"
    const priceHeaders = ["usd", "usd_foil", "euro", "euro_foil", "tix"]
    import { parseCurrency } from "../assets/functions";
    import {trackNewCard} from "../util/search"


</script>

{#await handleSubmit(params.query) then results}
<div class="flex flex-col">
    <h1 class="py-5">
        {results.length} {results.length > 1 ? "results" : "result"} for {params.query}
    </h1>

    <table class="table-auto  bg-gray-50 dark:bg-gray-700 outline outline-gray-700 rounded-lg">

            <thead class="border-b-2 border-black/50">
                <tr class="text-xs uppercase text-gray-700  dark:text-gray-400">
                        <th scope="col" class="px-6 py-3 text-left">
                            Name
                        </th>
                        <th scope="col" class="px-6 py-3 text-right">
                            Set
                        </th>
                    {#each priceHeaders as price}
                        <th scope="col" class="px-6 py-3 text-right">
                            {price.replace("_"," ")}
                        </th>
                    {/each}
                        <th scope="col" class="px-6 py-3 text-center">
                            Track
                        </th>
                </tr>
            </thead>

            <tbody class="bg-white text-gray-200 dark:bg-gray-800">
                {#each results as result}
                    <tr class="text-left not-last:border-b-2 border-gray-700 py-3 hover:bg-gray-700">

                        <th scope="row" class="px-4 py-2 font-medium text-gray-900 dark:text-white text-left">
                            {result.name}
                        </th>

                        <td class="px-6 py-2 white text-right">
                                {result.set_full}
                            <i class="ss text-xl ml-4 ss-{result.set.toLowerCase()}"></i>
                        </td>

                        {#each priceHeaders as price}

                            <td class="px-6 py-2 whitespace-preline text-right" style="font-variant-numeric: tabular-nums">
                                {parseCurrency(Number(result.prices[price]), price)}
                            </td>

                        {/each}

                        <td class="px-2 py-2 whitespace-preline text-center border-l border-gray-700">
                            <button class="bg-gray-600 border-black border px-4 rounded-md hover:bg-indigo-600 transition-colors"
                            on:click={() => trackNewCard(result)}>
                                Hello
                            </button>
                        </td>

                    </tr>
                {/each}
            </tbody>

    </table>
</div>
{/await}
