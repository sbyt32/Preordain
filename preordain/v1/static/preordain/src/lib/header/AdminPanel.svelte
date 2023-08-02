<script lang="ts">
  import HomeMenu from './HomePanel.svelte';

    import { push } from 'svelte-spa-router';



    function onKeyPress(e: KeyboardEvent, str: string) {
        if (e.code === 'Enter') push(`#/search/${str}`);
}

	$:searchQuery = ''
    $:dropdown = false
</script>

        <div class="place-self-center">
            <button class="component-theme w-fit px-3 py-1 text-base">
                Admin Panel
            </button>
        </div>


            <!-- <div>
      <button
            type="button"
            class="inline-flex gap-x-1.5 rounded-md bg-gray-200 px-3 py-2 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50" id="menu-button"
            aria-expanded="true"
            aria-haspopup="true"
            on:click={() => dropdown = !dropdown}>
        <svg class="-mr-1 h-5 w-5 text-gray-400" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
            <path fill-rule="evenodd" d="M5.23 7.21a.75.75 0 011.06.02L10 11.168l3.71-3.938a.75.75 0 111.08 1.04l-4.25 4.5a.75.75 0 01-1.08 0l-4.25-4.5a.75.75 0 01.02-1.06z" clip-rule="evenodd"/>
        </svg>
            {$projectName} {$envIsTest == true ? "(Testing)" : ""}
      </button>
    </div> -->

    <!--
      Dropdown menu, show/hide based on menu state.

      Entering: "transition ease-out duration-100"
        From: "transform opacity-0 scale-95"
        To: "transform opacity-100 scale-100"
      Leaving: "transition ease-in duration-75"
        From: "transform opacity-100 scale-100"
        To: "transform opacity-0 scale-95"
    -->
    <!-- {#if dropdown}
    <div class="absolute z-10 mt-2 w-56 place-self-center rounded-md origin-top bg-gray-500 shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none" role="menu" aria-orientation="vertical" aria-labelledby="menu-button" tabindex="-1">
      <div class="py-1 text-white" role="none">
        {#each [{route: "/", name: "Home"},{route: "/", name: "Inventory"},{route: "/", name: "Groups"}] as btn, i}
          <button on:click={() => push(btn.route)} class="block px-4 py-2 text-sm" role="menuitem" tabindex="-1" id="menu-item-{i}">{btn.name}</button>
        {/each}
      </div>
    </div>
  {/if} -->
