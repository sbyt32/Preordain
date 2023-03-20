<script lang="ts">
    import Row from "../lib/Row.svelte";
    import CardDash from "../lib/CardDash.svelte";
    import PriceGraph from '../lib/charts/PriceGraph.svelte';
    import Changes from '../lib/DailyChanges.svelte';
    import Table from '../lib/Table.svelte';
    import { projectTitle } from "../assets/stores";
    import GroupSelectedContainer from "../lib/groups/GroupSelectedContainer.svelte";


    export let params = {group: ""}

    projectTitle.set(`Group: ${params.group}`)
</script>

<!-- pb-6 because the top is already padded by 6 -->
<h1 class="pb-6 text-2xl font-semibold text-center">
    {params.group}
</h1>

    <Row>
        <svelte:fragment slot="Component">
            <CardDash col_span=3/>
            <GroupSelectedContainer/>
            <Changes col_span=1/>
            <!-- <PriceGraph col_span=3/> -->
            <Table col_span=3 group={params.group}/>
        </svelte:fragment>
    </Row>
