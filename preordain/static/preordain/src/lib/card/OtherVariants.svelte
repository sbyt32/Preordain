<script lang="ts">
    import { database } from "../../util/fetch_data";
    import { parseCurrency } from "../../util/dataFormatter";
    import { link } from "svelte-spa-router";
    export let params = null



</script>


<div class="component-theme w-1/3 text-center pb-4">
    <span class="font-semibold">Other Variants</span>

    <table class="table-auto w-full ">

        <thead class="border-b-2 border-b-slate-600">
            <tr>
                <th class="text-left pl-9"><i class="ss invisible ss-fw"/>Set</th>
                <th class="text-right pr-4">Price</th>
            </tr>
        </thead>

        <tbody>
            {#await database(`/price/variants/${params.set}/${params.cn}`)}
                <tr>
                    <td class="text-left">Loading...</td>
                    <td class="text-right">Loading...</td>
                </tr>
            {:then prices}
                {#each prices.data as price}
                <tr class="hover:bg-gray-600 not-last:border-b border-b-slate-600 ">
                    <td class="text-left pl-4 leading-loose text-sm">
                        <i class="ss ss-2x ss-{price.set} ss-{price.rarity} ss-fw ss-grad {price.usd == null && price.usd_foil ? "ss-foil" : "" }"/>
                        <a href="/card/{price.set}/{price.id}" use:link> {price.set_full}</a>
                    </td>
                    <td class="text-right tabular-nums pr-4">{price.usd ? parseCurrency(price.usd, "usd") : price.usd_foil ? `🌟 ${parseCurrency(price.usd_foil, "usd")}` : "N/A"}</td>
                </tr>
                {/each}
            {/await}
        </tbody>

    </table>
</div>
