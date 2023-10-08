<script lang="ts">
    import { link } from "svelte-spa-router";

// import { params } from "svelte-spa-router"
import { database } from "../../lib/connection"

interface searchQuery {
    query?: string
}
export let params:searchQuery = {}

</script>


<div class="max-sm:mx-0 mx-12 my-2">

    <div class="py-4">
        <h1 class="text-2xl">
            <!-- {data.post.length} result{data.post.length != 1 ? "s" : ""} for "{$page.params.query}" -->
        </h1>
    </div>

    {#await database(`info/search/${params.query}`) then data}

    <table class="table-auto w-full border border-black rounded-lg  max-sm:text-xs">
        <thead>
            <tr class="text-left">
                <th class="max-sm:px-2 px-6">Name</th>
                <th>Set</th>
                <th class="max-sm:after:content-['Col._#'] md:after:content-['Collector_#']"></th>
                <th>Current Price</th>
            </tr>
        </thead>
        <tbody class="divide-y divide-dashed divide-black">
            {#each data as cardData}
                <tr class="">
                    <td class="max-sm:px-2 px-6"><a href="/card/{cardData.card_data.set_code}/{cardData.card_data.collector_number}" use:link>{cardData.card_data.card_name}</a></td>
                    <td class="uppercase">{cardData.card_data.set_code}</td>
                    <td>{cardData.card_data.collector_number}</td>
                    <td class="tabular-nums">{cardData.prices.usd == null ? "N/A" : `$${cardData.prices.usd}`}</td>
                </tr>
            {/each}
        </tbody>
    </table>
    {/await}

</div>
