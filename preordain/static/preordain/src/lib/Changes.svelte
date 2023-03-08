<script lang="ts">
import { database } from "../fetch_data"
import { parsePercentage } from "../assets/functions";
export let col_span: string | number = 1

$: current = "DESC"
let selectedClasses = "inline-block p-4 text-blue-600 bg-gray-100 rounded-t-lg active dark:bg-gray-800 dark:text-blue-500"
let allClasses = "inline-block p-4 rounded-t-lg hover:text-gray-600 hover:bg-gray-50 dark:hover:bg-gray-800 dark:hover:text-gray-300"
</script>

<span style="grid-column: span {col_span} / span {col_span}" class="shadow-2xl h-full component-theme row-span-2">
    <ul class="flex flex-wrap text-sm font-medium text-center text-gray-500 border-b border-gray-200 dark:border-gray-700 dark:text-gray-400">
        <li class="mr-2">
            <button class="{current === 'DESC' ? selectedClasses: allClasses}"  on:click={() => current = "DESC"}>
                Gains
            </button>
        </li>
        <li class="mr-2">
            <button class="{current === 'ASC' ? selectedClasses: allClasses}" on:click={() => current = "ASC"}>
                Losses
            </button>
        </li>
    </ul>

    <table>
        <thead class="table w-full table-fixed px-2">
            <tr class="text-xs uppercase text-gray-700  dark:text-gray-400">
                {#each ["Name","Set"," % Change"] as titles}
                    <th scope="col" class="px-6 py-3">
                        {titles}
                    </th>
                {/each}
            </tr>
        </thead>
        <tbody class="block bg-white text-gray-200 dark:bg-gray-800 rounded-lg px-2">
            {#key current}
                {#await database(`http://localhost:8000/api/price/changes/${current}/`)}
                <tr class="table w-full table-fixed dark:border-gray-700 border-b text-sm">
                    <td>
                        Loading...
                    </td>
                </tr>
                {:then data}
                    {#each data.data as change}
                    <tr class="table w-full table-fixed dark:border-gray-700 border-b text-sm">
                        <td class="text-ellipsis whitespace-nowrap overflow-hidden">
                            {change.name}
                        </td>
                        <!-- Set Image -->
                        <td class="text-center">
                            <i class="ss text-xl ss-{change.set}"></i>
                        </td>
                        <td class="text-right">
                            {@html parsePercentage(change.usd_change)}
                        </td>
                    </tr>
                    {/each}
                {/await}
            {/key}
        </tbody>
    </table>

</span>
