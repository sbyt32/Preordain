<script>
  import "../app.postcss";
  import Icon from '@iconify/svelte';
  import {displaySidebar} from "$lib/stores"
  import NavigatonSidebar from '../components/NavigatonSidebar.svelte';

</script>


{#if $displaySidebar}
  <NavigatonSidebar/>
{/if}

<div class="w-screen bg-indigo-700 py-2 text-white inline-flex">

  <button on:click={() => $displaySidebar = !$displaySidebar}>
    <Icon icon="material-symbols:density-medium-rounded" height=32 width=32/>
  </button>

  <h1 class="text-center grow text-lg">
    {#key displaySidebar}
      {$displaySidebar}
    {/key}
  </h1>

</div>
<slot />
