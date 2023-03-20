<script>
    import Row from "../lib/Row.svelte";
    import CardDash from "../lib/CardDash.svelte";
    import PriceGraph from '../lib/charts/PriceGraph.svelte';
    import Changes from '../lib/DailyChanges.svelte';
    import Table from '../lib/Table.svelte';
    import {location} from 'svelte-spa-router'
    import { projectTitle } from "../assets/stores";

    projectTitle.set("Home")
</script>

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
