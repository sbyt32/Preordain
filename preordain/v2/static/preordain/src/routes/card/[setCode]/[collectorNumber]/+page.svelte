<script lang="ts">
    import type { PageData } from './$types';
    // import { page } from "$app/stores"

    export let data: PageData
</script>

<!-- {#await data.price then card}
    <h1>
        {card}
    </h1>
{/await} -->

<table class="table-auto w-full">
    <thead>
        <tr>
            <th>Date</th>
            <th>USD</th>
            <th>USD (Foil)</th>
            <th>USD (Etched)</th>
            <th>Euro</th>
            <th>Euro (Foil)</th>
            <th>TIX</th>
        </tr>
    </thead>
    <tbody>
    {#each data.price as card}
        <tr>
            <td>{card.date}</td>
            {#each Object.values(card.prices) as priceType}
                <td>{priceType}</td>
            {/each}
        </tr>
    {/each}
    </tbody>
</table>
