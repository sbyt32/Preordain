<script lang="ts">
    import type { CardInfoResponse } from "$lib/responses";
    export let imgURL: string, cardData: CardInfoResponse;

    // const
</script>

<div class="h-80 flex gap-4 my-4">

    <img src="{imgURL}" alt="" class="object-contain shadow-2xl">

    <div class="outline outline-1 shadow-2xl w-full rounded-md px-5 py-2 inline-flex flex-col">

        <!-- Headers -->
        <h2 class="text-3xl pt-1">
            {cardData.card_data.card_name}
        </h2>

        <span class="grid grid-cols-2 border-b-[1.5px] border-b-gray-400">
            <h4 class="text-lg text-black/80 text-start">
                <!-- {cardData.card_data.} -->
                PLACEHOLDER
            </h4>
            <h4 class="text-lg text-black/80 text-end">
                <!-- {cardData.card_data} -->
                PLACEHOLDER
            </h4>
        </span>

        <div class="text-xl grow py-1">
            {cardData.card_data.oracle_text}
            <!-- <p>Surveil 1. (Look at the top card of your library. You may put that card into your graveyard.)</p>
            <p>Draw a card.</p> -->
        </div>

        <div class="border-t-[1.5px] border-t-gray-400 text-black/80 text-end py-1">
            #{cardData.card_data.collector_number} Artist: {cardData.card_data.artist}
        </div>
    </div>
    <div class="outline outline-1 shadow-2xl w-[444px] rounded-md px-5 pt-3 pb-2 flex flex-col">
        <!-- first:border-t-0 border-t border-t-black -->
        <div class="inline-grid grid-cols-2 gap-0.5 capitalize">
            {#each Object.keys(cardData.legalities) as format}
                <p class="">{format}</p>
                <p class=" rounded-lg bg-green-600 text-center text-white">{cardData.legalities[format]}</p>
            {/each}
        </div>
        <!-- <table class="table-fixed capitalize border-collapse">
            {#each Object.keys(cardData.legalities) as format}
            <tr class="border-b-[0.5px] border-b-gray-400 rounded-md">
                <td class="w-1/2">{format}</td>
                <td class="rounded-lg bg-green-600 text-center text-white">{cardData.legalities[format]}</td>
            </tr>
            {/each}
        </table> -->

        <div class="grow"/>

        <span class="border-t-[1.5px] border-t-gray-400 pt-2">
            <div class="bg-black rounded-md inline-flex gap-1 w-full outline outline-1">
                <button class="bg-gray-400 rounded-l-md w-1/2 hover:bg-blue-200">
                    + Collection
                </button>
                <button class="bg-gray-400 rounded-r-md w-1/2 hover:bg-blue-200">
                    Set Price Alert
                </button>
            </div>

        </span>
    </div>
</div>
