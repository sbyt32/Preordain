<script lang="ts">
  import "../app.postcss";
  import Icon from '@iconify/svelte';
  import {displaySidebar} from "$lib/stores"
  import NavigatonSidebar from '../components/NavigatonSidebar.svelte';
  import { connectURL } from "$lib";
  import { goto } from "$app/navigation";
  $: query = ""

  function onKeyPress(e: KeyboardEvent, query: string) {
    if (e.code === "Enter") goto(`/search/${query}`)
  }
</script>


{#if $displaySidebar}
  <NavigatonSidebar/>
{/if}

<div class="w-screen bg-indigo-700 py-2 text-white inline-flex drop-shadow-lg px-4">

  <button on:click={() => $displaySidebar = !$displaySidebar} class="pr-2">
    <Icon icon="material-symbols:density-medium-rounded" height=32 width=32/>
  </button>

  <h1 class="text-center grow text-xl">
    <input
      type="text"
      name="query"
      class="text-black px-2
        placeholder-shown:italic rounded-md
        w-1/3 max-sm:w-full
        my-2"
      placeholder="Search Query"
      bind:value={query}
      on:keydown={(e) => onKeyPress(e, query)}
    >
  </h1>

</div>

<main>
  <slot />
</main>
