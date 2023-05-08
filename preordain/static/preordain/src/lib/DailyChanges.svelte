<script lang="ts">
import { database } from "../util/fetch_data"
import { parsePercentage } from "../util/parseValues";
import { CurrentCard, connectURL } from "../assets/stores";
export let col_span:number | string = 1
export let row_span:number | string = 2


let selectedClasses = "inline-block p-4 text-blue-600 bg-gray-100 rounded-t-lg active dark:bg-gray-800 dark:text-blue-500"
let allClasses = "inline-block p-4 rounded-t-lg hover:text-gray-600 hover:bg-gray-50 dark:hover:bg-gray-800 dark:hover:text-gray-300"

const tabs = [
    {currency: "USD", direction: "DESC"},
    {currency: "USD", direction: "ASC"},
    {currency: "Euro", direction: "DESC"},
    {currency: "Euro", direction: "ASC"},
]

$: current = tabs[0]

</script>

<div style="grid-column: span {col_span} / span {col_span}; grid-row: span {row_span} / span {row_span};" class="shadow-2xl min-h-0 component-theme flex flex-col">

    <div class="text-center text-base font-medium border-b-4 border-b-gray-700 py-2 h-fit">
        Top Gains / Losses
    </div>

    <div class="h-fit">
        <ul class="flex flex-row font-medium text-sm text-center text-gray-500 border-b border-gray-200 dark:border-gray-700 dark:text-gray-400 overflow-x-auto">
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
    </div>


    <table class="bg-gray-50 dark:bg-gray-700 h-full overflow-hidden rounded-b-md flex flex-col" >

        <thead class="border-b-2 border-black/50 table table-fixed" style="width: calc(100% - .75em);">
            <tr class="text-xs uppercase text-gray-700 dark:text-gray-400 w-full">
                {#each ["Name","Set"," % Change"] as titles}
                    <th scope="col" class="px-6 py-3 first:text-left text-right">
                        {titles}
                    </th>
                {/each}
            </tr>
        </thead>
        <tbody class="bg-white text-gray-200 dark:bg-gray-800 overflow-y-auto grow font-light scrollbar rounded-b-lg">
            {#key current}
                {#await database(`${$connectURL}/price/changes/${current.direction.toLowerCase()}/${current.currency.toLowerCase()}/`)}
                <tr class="table w-full table-fixed dark:border-gray-700 border-b text-sm">
                    <td class="px-6 py-3 text-white text-left text-xs font-semi-bold cursor-pointer  transition-colors animate-pulse">
                        loading...
                    </td>
                </tr>
                {:then data}
                    {#each data.data as change}
                    <tr class="not-last:border-b-2 border-gray-700 w-full table table-fixed">
                        <th scope="row" class="px-6 py-3 text-gray-900 dark:text-white text-left text-xs font-semi-bold cursor-pointer hover:text-blue-400 transition-colors" on:click={() => {$CurrentCard = {set_name: change.set, card: change.name, id: change.id}}}>
                                {change.name}
                        </th>
                        <!-- Set Image -->
                        <td class="px-5 py-2 text-right whitespace-preline tabular-nums">
                            <div class=" font-normal group relative">
                                <i class="ss text-2xl ss-{change["set"]} ss-rare ss-fw"></i>
                                <div class="absolute py-1 px-2 z-10 w-fit text-base h-min text-white text-center bg-gray-700 border rounded-md invisible opacity-0 transition-opacity duration-500 group-hover:visible group-hover:opacity-100 ">

                                    <p class="relative">{change.set_full}</p>
                                </div>
                            </div>
                        </td>
                        <td class="px-5 py-2 text-right text-base">
                            {@html parsePercentage('usd_change' in change ? change.usd_change : change.euro_change)}
                        </td>
                    </tr>
                    {/each}
                {/await}
            {/key}
        </tbody>
    </table>

</div>
