<script>
  import Icon from "@iconify/svelte"
  import {displaySidebar} from "$lib/stores"

  const tabData = [
    {
      name: "Home",
      icon: "",
      route: "/"
    },
    {
      name: "Decks",
      icon: "",
      route: "/"
    },
    {
      name: "Inventory",
      icon: "",
      route: "/"
    },
    {
      name: "Tracking",
      icon: "",
      route: "/"
    },
    {
      name: "Sales",
      icon: "",
      route: "/"
    },
    {
      name: "Settings",
      icon: "",
      route: "/"
    }
  ]
</script>

<div class="h-screen w-screen absolute">
    <!-- TODO: Add esc to close site -->
    <!-- svelte-ignore a11y-click-events-have-key-events -->
    <!-- svelte-ignore a11y-no-static-element-interactions -->
    <div class="h-screen w-screen bg-gray-700 opacity-80 absolute" on:click={() => $displaySidebar = !$displaySidebar} />

      <!-- Sidebar -->
      <div class="h-screen bg-indigo-700 w-1/4 absolute text-white">

        <button on:click={() => $displaySidebar = !$displaySidebar} class="text-white py-2">
          <Icon icon="material-symbols:density-medium-rounded" height=32 width=32/>
        </button>

        <div class="flex flex-col">
          {#each tabData as tab}
            <h2 class="text-lg">
              {tab.name}
            </h2>
          {/each}
        </div>

      </div>

</div>
