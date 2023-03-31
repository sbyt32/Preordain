<script lang="ts">
	import { fly } from 'svelte/transition';
    import { showPopup } from './stores';
    import type { ComponentType } from 'svelte';
</script>
{#if $showPopup.display}
<div class="z-10 absolute bottom-4 bg-inherit/20 w-full h-1/5" transition:fly="{{duration: 500, opacity: 0}}">
    <div class="h-full flex flex-row-reverse">

        <div class="text-center font-light w-1/2 relative">

            <button on:click={() => showPopup.close()} class="preordain-button top-0.5 ml-0.5 right-0 h-1/4 border-0 border-transparent absolute opacity-40 hover:opacity-100 transition-opacity">
            Close
            </button>
            <svelte:component this={$showPopup.component}/>

        </div>
    </div>
</div>
{/if}
