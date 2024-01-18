<script lang="ts">
    import type { PageData } from './$types';
    import { page } from "$app/stores"

    export let data: PageData

</script>


<div class="max-sm:mx-0 mx-12 my-2">

    <div class="py-4">
        <h1 class="text-2xl">
            {data.post.length} result{data.post.length != 1 ? "s" : ""} for "{$page.params.query}"
        </h1>
    </div>

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
            {#each data.post as cardData}
                <tr class="">
                    <td class="max-sm:px-2 px-6"><a href="/card/{cardData.card_data.set_code}/{cardData.card_data.collector_number}">{cardData.card_data.card_name}</a></td>
                    <td class="uppercase">{cardData.card_data.set_code}</td>
                    <td>{cardData.card_data.collector_number}</td>
                    <td class="tabular-nums">{cardData.prices.usd == null ? "N/A" : `$${cardData.prices.usd}`}</td>
                </tr>
            {/each}
        </tbody>
    </table>
</div>
