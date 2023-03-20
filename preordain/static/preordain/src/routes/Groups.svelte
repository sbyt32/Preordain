<script lang="ts">
    import GroupContainer from '../lib/groups/GroupContainer.svelte';

    import { connectURL, projectTitle } from "../assets/stores";
    import { database } from "../util/fetch_data";
    let filterInUse = false

    $: groupInfo = database(`${$connectURL}/groups/?in_use=${filterInUse}`)

    export const params = {}

    projectTitle.set("Groups")
</script>

<div class="flex flex-row h-2/3">

    <div class="basis-2/12 shrink-0 component-theme">
        <div class="flex flex-col  h-full">

            <div class="text-center text-2xl font-semibold border-b-2 border-gray-700 w-full pb-2 self-center basis-3 py-4">
                Search Stuff
            </div>

            <div class="inline-flex grow">
                <ul class="list-none list-item mx-8">

                    <li>
                        <label class="text-xl select-none cursor-pointer">
                            <input type="checkbox" class="mr-2" bind:checked={filterInUse}>
                            In Use
                        </label>
                    </li>

                </ul>

            </div>

            <div class="w-full text-center border-t-2 border-gray-700 py-4">
                <button class="preordain-button">
                    Add Group
                </button>
            </div>

        </div>
    </div>

    <div class="component-theme mx-8">
        <div class="grid grid-cols-4 grid-rows-3 gap-4 text-center m-4">
            {#await groupInfo then groupQuery}
                {#each groupQuery.data as groupData}
                    <GroupContainer groupData={groupData}/>
                {/each}
            {/await}
            {#each [1,2,3,4,5,6,7] as _}
                <GroupContainer/>
            {/each}
            <GroupContainer groupData={
            {
                group: "scripasdasdsadsaddsasadsdhjkasdhjsdhjksdhjkasdhjasdhjkasdasdsddhjkasdhjhjkasdtion",
                description: "scripasdasdsadsaddsasadsdhjkasdhjsdhjksdhjkasdhjasdhjkasdasdsddhjkasdhjhjkasdtion",
                cards_in_group: 69420
            }}/>

        </div>
    </div>



</div>
