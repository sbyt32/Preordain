
<script lang="ts">
    import { database } from "../util/fetch_data";

    function parseEventType(event_type: string) {
        switch (event_type) {
            case "mtgo":
                return "💻"
            case "paper":
                return "🃏"
            case "mtga":
                return "🅰️"
            default:
                return "❔";
        }
    }

</script>

<div class="col-span-3 row-span-1 component-theme">


    <!-- <div class="p-4">
        asd
    </div> -->

    <!-- <div class="flex flex-col"> -->

        <table class="h-full rounded-b-md flex flex-col">

            <div class="text-center pt-1 border-b-1">
                <h1 class="font-semibold text-xl">Recent Events</h1>
            </div>


            <thead class="border-b-2 border-black/50 table-fixed table" >
                <tr class="text-xs uppercase text-gray-700 dark:text-gray-400 w-full flex ">
                    <th scope="col" class="px-7 py-3 whitespace-preline text-left mx-0 w-fit">Type</th>
                    <th scope="col" class="px-5 py-3 whitespace-preline text-left mx-0 w-fit">Format</th>
                    <th scope="col" class="px-7 pl-12 py-3 whitespace-preline text-left mx-0">Date</th>
                    <th scope="col" class="pl-20 px-7 py-3 whitespace-preline text-left mx-0 grow">Event</th>
                </tr>
            </thead>
            <tbody class="dark:bg-gray-800 overflow-y-auto grow font-light scrollbar rounded-b-lg">
                {#await database("/events/")}
                    <tr class="not-last:border-b-2 last:pb-2 first:pt-1 border-gray-700 w-full flex hover:bg-gray-600">
                        <td>asd</td>
                        <td>asd</td>
                        <td>asd</td>
                    </tr>
                {:then events}
                    {#each events.data as event}
                        <tr class="not-last:border-b-2 last:pb-2 first:pt-1 border-gray-700 w-full flex hover:bg-gray-600 border-r-2">
                            <td class="px-7 mx-0 text-left whitespace-preline">{parseEventType(event.event_type)}</td>
                            <td class="px-7 mx-0 text-left whitespace-preline">{event.format}</td>
                            <td class="px-7 mx-0 text-left whitespace-preline tabular-nums">{event.event_date}</td>
                            <td class="px-7 pl-8 mx-0 text-left whitespace-preline grow"><a href={event.url} class="">{event.event_name}</a></td>
                        </tr>
                {/each}
                {/await}
            </tbody>
        </table>

    <!-- </div> -->

</div>

<!--
<table class="bg-gray-50 dark:bg-gray-700 h-full component-theme rounded-b-md flex flex-col" >

    <thead class="border-b-2 border-black/50 table table-fixed" style="width: calc(100% - .75em);">

        <tr class="text-xs uppercase text-gray-700 dark:text-gray-400 w-full">
                <th scope="col" class="px-7 py-3 first:text-left text-right mx-0">
                    {titles}
                </th>
        </tr>

    </thead>

        <tbody class="bg-white text-gray-200 dark:bg-gray-800 overflow-y-auto grow font-light scrollbar rounded-b-lg">

            {#each parseData(groupData) as card_data}
                <tr class="not-last:border-b-2 border-gray-700 w-full table table-fixed group">
                    {#each header as data_type}
                        {#if data_type === "Name"}
                            <th scope="row" class="px-6 py-2 text-white text-left cursor-pointer group-hover:text-indigo-500 hover:underline transition-all" on:mousemove={() => updateCardDash(card_data)}>
                                {card_data["Name"]}
                            </th>
                        {:else}
                        <td class="px-6 text-right whitespace-preline tabular-nums">
                            {@html parseRow(card_data, data_type)}
                        </td>
                        {/if}
                    {/each}
                </tr>
            {/each}

        </tbody>


</table> -->
