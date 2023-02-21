<script lang="ts">
  import CardDash from './lib/CardDash.svelte';
  import Table from './lib/Table.svelte';
  import { database } from './fetch_data';
</script>

<main>
    <div class="text-2xl text-center">Preordain</div>

    <div class="container mx-auto">
        <div class="grid grid-cols-2 grid-rows-1 gap-4">
            <span class="pt-6 row-span-2 col-span-2 inline-grid grid-cols-4 grid-rows-1 gap-4">
                <span class="col-span-3">
                    {#await database('http://127.0.0.1:5000/api/price/vow/38?max=1') then prices}
                        <CardDash data={prices}/>
                    {/await}
                </span>
                <span>1</span>
            </span>
            <span class="col-span-2 w-full">
                {#await database('http://127.0.0.1:5000/api/card/') then data}
                    <Table data={data}/>
                {/await}
            </span>
        </div>
  </div>
</main>
