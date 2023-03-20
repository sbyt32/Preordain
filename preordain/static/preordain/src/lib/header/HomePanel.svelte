<script lang="ts">
    import { push } from 'svelte-spa-router';
</script>


<div class="relative text-center place-self-center ">
  <div class="text-center place-self-center text-white gap-4 font-semibold">
    {#each [{route: "/", name: "Home"},{route: "/inventory/", name: "Inventory"},{route: "/groups/", name: "Groups"}] as btn, i}
      <button on:click={() => push(btn.route)} class="not-last:mr-10">{btn.name}</button>
    {/each}
  </div>
</div>
