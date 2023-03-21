<script lang="ts">
	import { fly } from 'svelte/transition';
    import { showPopup } from './stores';
    import CardDash from '../lib/CardDash.svelte';
    import type { ComponentType } from 'svelte';
    export let popupComponent: ComponentType = CardDash;

</script>

{#if $showPopup}
<div class="z-10 absolute bottom-5 bg-inherit/20 w-full h-1/5" transition:fly="{{duration: 500, opacity: 0}}">
    <div class="relative  h-full flex flex-row-reverse">

        <div class="text-center font-light w-1/2">
            <svelte:component this={popupComponent}/>
        </div>
        <button on:click={() => showPopup.close()} class="preordain-button h-1/4 rounded-none border-0 border-transparent">
            Close
        </button>
    </div>
</div>
{/if}
