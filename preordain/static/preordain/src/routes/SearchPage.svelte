<script lang="ts">
    export let params = {"query": ""};

    import {handleSubmit, untrackOldCard} from "../util/search"
    const priceHeaders = ["usd", "usd_foil", "euro", "euro_foil", "tix"]
    import { currentTab, projectTitle, showPopup } from "../assets/stores";
    import { parseCurrency } from "../util/dataFormatter";
    import {trackNewCard} from "../util/search"
    import Error from "../lib/Error.svelte";
    import { onDestroy } from "svelte";
    import { link, push } from "svelte-spa-router";
    projectTitle.set(`Search: ${params.query}`)
    $currentTab = "Search"
    onDestroy(() => {
        showPopup.close()
    })
</script>


<div class="flex flex-col">
    {#await handleSubmit(params.query) then results}

    <h1 class="py-5 text-2xl font-semibold">
        {results.length} {results.length == 1 ? "result" : "results"} for "{params.query}"
    </h1>

    <table class="table-auto bg-gray-50 dark:bg-gray-700 outline outline-gray-700 rounded-lg">

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

            <tbody class="text-gray-200 bg-gray-800">
                {#each results as result}
                    <tr class="text-left not-last:border-b-2 border-gray-700 py-3 hover:bg-gray-700">

                        <th scope="row" class="px-4 py-2 font-medium text-white text-left">
                            <a href="/card/{result.set}/{result.id}" use:link class="hover:text-indigo-500 transition-colors">
                                {result.name}
                            </a>
                        </th>

                        <td class="px-6 py-2 white text-right">
                                {result.set_full}
                            <i class="ss text-xl ml-4 ss-{result.set.toLowerCase()} ss-rare"></i>
                        </td>

                        {#each priceHeaders as price}

                            <td class="px-6 py-2 whitespace-preline text-right" style="font-variant-numeric: tabular-nums">
                                {parseCurrency(Number(result.prices[price]), price)}
                            </td>

                        {/each}

                        <td class="px-2 py-2 whitespace-preline text-center border-l border-gray-700">
                            <button class="bg-gray-600 border-black border px-4 rounded-md preordain-button"
                            disabled='{result["scrape_sales"]}'
                            on:click={() => trackNewCard(result)}>
                                Track
                            </button>
                            <button class="bg-gray-600 border-black border px-4 rounded-md preordain-button delete"
                            disabled='{!result["scrape_sales"]}'
                            on:click={() => untrackOldCard(result)}>
                                Untrack
                            </button>
                        </td>

                    </tr>
                {/each}
            </tbody>
    </table>
    {:catch}
    <h1 class="py-5 text-2xl font-semibold">
        0 results for "{params.query}"
    </h1>
    <Error/>
{/await}
</div>
