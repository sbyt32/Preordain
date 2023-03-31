<script lang="ts">
    import { push } from "svelte-spa-router";


    export let groupData = {group: "Sample", description: "Sample Description", cards_in_group: 123}
</script>


<!-- svelte-ignore a11y-click-events-have-key-events -->
<div class="bg-slate-600 p-2 place-content-center font-normal rounded-md hover:shadow-lg hover:shadow-black/40 transition-all duration-300 text-base group cursor-pointer" on:click={() => push(`/groups/${groupData.group}`)}>
    <img src="https://placekitten.com/g/500/200" class="object-scale-down self-center border rounded-xl border-indigo-600 shadow-amber-600 shadow-sm group-hover:shadow-lg group-hover:shadow-amber-600 transition-shadow" height="200px" width="500px" alt="sample">
    <h1 class="text-ellipsis overflow-hidden whitespace-nowrap text-xl font-bold mt-1.5 ">{groupData.group}</h1>
    <br>
    <p class="text-ellipsis overflow-hidden whitespace-nowrap">{groupData.description}</p>
    <p class="text-ellipsis overflow-hidden whitespace-nowrap italic text-sm">Cards in Group: {groupData.cards_in_group}</p>
</div>
