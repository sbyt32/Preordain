<script lang="ts">
    import Row from "../lib/Row.svelte";
    import CardDash from "../lib/CardDash.svelte";
    import PriceGraph from '../lib/charts/PriceGraph.svelte';
    import Changes from '../lib/DailyChanges.svelte';
    import Table from '../lib/Table.svelte';
    import { projectTitle } from "../assets/stores";

    let loaded = false


    export const params = {}

    projectTitle.set("Groups")
</script>


{#if loaded}
    <div class="grid grid-cols-4 grid-rows-4 h-2/3">
        <Row>
            <svelte:fragment slot="Component">
                <CardDash col_span=3/>
                <Changes col_span=1/>
                <PriceGraph col_span=3/>
                <!-- <Table col_span=3/> -->
            </svelte:fragment>
        </Row>
        <!-- <Row>
            <svelte:fragment slot="Component">
                <PriceGraph col_span=3/>
            </svelte:fragment>
        </Row> -->
    </div>
{/if}
