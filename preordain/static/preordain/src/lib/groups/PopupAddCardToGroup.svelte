<script lang="ts">
    import { connectURL } from "../../assets/stores";
    import GroupSelectedContainer from "./selected/GroupSelectedContainer.svelte";
    import type { PostGroupsNew } from "./interfaces";


    async function addNewGroup(params:PostGroupsNew) {

        await fetch(`${$connectURL}/groups/new/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "write": "testing"
            },
            body: JSON.stringify(params)
        }).then((data) => {
            if (data.status == 201) {
                return true
            }
            else {
                return false
            }
        })
    }

    $: params = {
        group_name: "",
        description: ""
    }
</script>

<div class="h-full flex flex-row-reverse">
    <div class="component-theme container basis-1/2 py-2 px-2 flex flex-col gap-3">
        <h1>Add a group</h1>
        <input type="text" placeholder="Group Name" class="p-2" bind:value={params.group_name}>
        <input type="text" placeholder="Short Description..." class="px-2 py-3" bind:value={params.description}>
        <div class="inline-flex">
            <button class="preordain-button basis-1/3 shrink-0 py-2" disabled="{!params.description && !params.group_name}" on:click={() => addNewGroup(params)}>Submit!</button>
            <p class="mx-4 grow component-theme w-full border-red-600 py-2">add pass or failed</p>
        </div>
    </div>

</div>
