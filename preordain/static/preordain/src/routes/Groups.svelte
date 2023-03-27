<script lang="ts">
    import GroupContainer from '../lib/groups/GroupContainer.svelte';

    import { connectURL, currentTab, projectTitle, showPopup } from "../assets/stores";
    import { database } from "../util/fetch_data";
    import PopupModifyGroup from '../lib/groups/PopupModifyGroups.svelte';
    import { onDestroy } from 'svelte';
    let filterInUse = false

    $: groupInfo = database(`${$connectURL}/groups/?in_use=${filterInUse}`)

    export const params = {}

    projectTitle.set("Groups")
    $currentTab = "Groups"
    onDestroy(() => {
        showPopup.close()
    })
</script>

<div class="flex flex-row h-full">

    <div class="basis-2/12 shrink-0 component-theme">
        <div class="flex flex-col h-full">

            <div class="text-center text-2xl font-semibold border-b-2 border-gray-700 w-full pb-2 self-center basis-3 py-4">
                Search Filters
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
                <button class="preordain-button" on:click={() => showPopup.show(PopupModifyGroup)}>
                    Add Group
                </button>
                <button class="preordain-button delete" on:click={() => showPopup.show(PopupModifyGroup)}>
                    Delete Group
                </button>
            </div>

        </div>
    </div>

    <div class="component-theme mx-8 grow">
        <div class="grid grid-cols-4 grid-rows-3 gap-4 text-center m-4">
            {#await groupInfo}
                <GroupContainer/>
            {:then groupQuery}
                {#each groupQuery.data as groupData}
                    <GroupContainer groupData={groupData}/>
                {/each}
            {/await}

        </div>
    </div>



</div>
