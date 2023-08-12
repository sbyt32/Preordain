<script>
  import Icon from "@iconify/svelte"
  import {displaySidebar} from "$lib/stores"


  const tabData = [
    { name: "Home", icon: "material-symbols:home", route: "/" },
    { name: "Decks", icon: "game-icons:stack", route: "/" },
    { name: "Inventory", icon: "material-symbols:inventory-2-sharp", route: "/" },
    { name: "Tracking", icon: "mdi:chart-line", route: "/" },
    { name: "Sales", icon: "mdi:cash-multiple", route: "/" },
    { name: "Settings", icon: "mdi:gear", route: "/" }
  ]
</script>

<div class="h-screen w-screen absolute z-20">
    <!-- TODO: Add esc to close site -->
    <!-- svelte-ignore a11y-click-events-have-key-events -->
    <!-- svelte-ignore a11y-no-static-element-interactions -->
    <div class="h-screen w-screen bg-gray-700 opacity-80 absolute" on:click={() => $displaySidebar = !$displaySidebar} />

      <!-- Sidebar -->
      <div class="h-screen bg-gray-700 max-sm:w-4/5 w-1/4 absolute text-white">

        <button on:click={() => $displaySidebar = !$displaySidebar} class="text-white py-2 pl-4">
          <Icon icon="material-symbols:density-medium-rounded" height=32 width=32/>
        </button>

        <h2 class="text-2xl mx-6 py-3 border-b border-black">
          Preordain
        </h2>
        <div class="flex flex-col gap-4 mx-6 pt-4">
          {#each tabData as tab}
            <h2 class="text-xl flex flex-row gap-2 hover:text-2xl transition-all">
              <Icon icon={tab.icon} height=24 width=24/>
              <a href={tab.route} class="" on:click={() => $displaySidebar = !$displaySidebar}>
                {tab.name}
              </a>
            </h2>
          {/each}
        </div>

      </div>

</div>
