<script lang="ts">
import { database } from "../fetch_data"
import { parsePercentage } from "../assets/functions";
import { CurrentCard } from "../assets/functions";
export let col_span: string | number = 1


let selectedClasses = "inline-block p-4 text-blue-600 bg-gray-100 rounded-t-lg active dark:bg-gray-800 dark:text-blue-500"
let allClasses = "inline-block p-4 rounded-t-lg hover:text-gray-600 hover:bg-gray-50 dark:hover:bg-gray-800 dark:hover:text-gray-300"

const tabs = [
    {currency: "USD", direction: "DESC"},
    {currency: "USD", direction: "ASC"},
    {currency: "Euro", direction: "DESC"},
    {currency: "Euro", direction: "ASC"},
]

$: current = tabs[0]
const connectURL = import.meta.env.VITE_CONNECTION;

</script>

<span style="grid-column: span {col_span} / span {col_span}" class="shadow-2xl h-full component-theme row-span-2">

    <div class="text-center text-base font-medium border-b-4 border-b-gray-700 py-2">
        Top Gains / Losses
    </div>

    <ul class="flex flex-row font-medium text-center text-gray-500 border-b border-gray-200 dark:border-gray-700 dark:text-gray-400">
        {#each tabs as tab}
        <li class="mr-2 not-last:border-r-2 dark:border-r-gray-700" >
            <button class="{current === tab ? selectedClasses: allClasses}" on:click={() => current = tab}>
                {tab.currency}
                <span class="text-xs">
                    ({tab.direction})
                </span>
            </button>
        </li>
        {/each}
    </ul>

    <table class="flex flex-col">
        <thead class="px-2 border-b-gray-700 border-b-4 mb-2">
            <tr class="text-xs uppercase text-gray-700 dark:text-gray-400 flex flex-row">
                {#each ["Name","Set"," % Change"] as titles}
                    <th scope="col" class="px-2 py-3 first:text-left text-right first:basis-3/6 first:shrink-0 basis-1/6 last:shrink-0 last:grow">
                        {titles}
                    </th>
                {/each}
            </tr>
        </thead>
        <tbody class="bg-white text-gray-200 dark:bg-gray-800 rounded-lg px-2">
            {#key current}
                {#await database(`${connectURL}/price/changes/${current.direction}/${current.currency}/`)}
                <tr class="table w-full table-fixed dark:border-gray-700 border-b text-sm">
                    <td>
                        Loading...
                    </td>
                </tr>
                {:then data}
                    {#each data.data as change}
                    <tr class="flex flex-row dark:border-gray-700 border-b text-sm">
                        <td class="text-ellipsis whitespace-nowrap overflow-hidden text-left basis-3/6 px-2" >
                            <button on:click={() => {$CurrentCard = {set_name: change.set, card: change.name, id: change.id}}}>
                                {change.name}
                            </button>
                        </td>
                        <!-- Set Image -->
                        <td class="text-right basis-1/6 shrink-0">
                            <i class="ss px-2 text-xl ss-{change.set}"></i>
                        </td>
                        <td class="text-right shrink-0 grow px-2">
                            {@html parsePercentage('usd_change' in change ? change.usd_change : change.euro_change )}
                        </td>
                    </tr>
                    {/each}
                {/await}
            {/key}
        </tbody>
    </table>

</span>
