<script lang="ts">
    import Row from "../lib/Row.svelte";
    import CardDash from "../lib/CardDash.svelte";
    import PriceGraph from '../lib/charts/PriceGraph.svelte';
    import Changes from '../lib/DailyChanges.svelte';
    import Table from '../lib/Table.svelte';
    import { projectTitle } from "../assets/stores";
    import GroupSelectedContainer from "../lib/groups/selected/GroupSelectedContainer.svelte";
    import testThalia from '/test_thalia.jpg';
    import GroupSelectedBanner from "../lib/groups/selected/GroupSelectedBanner.svelte";


    export let params = {group: ""}

    projectTitle.set(`Group: ${params.group}`)
</script>

<!-- pb-6 because the top is already padded by 6 -->
<!-- <h1 class="pb-6 text-2xl font-semibold text-center">
    {params.group}
</h1> -->


    <Row row_span={4} col_span={4}>
        <svelte:fragment slot="Component">
            <GroupSelectedBanner img={testThalia} groupName={params.group}/>

            <CardDash col_span={3} row_span={1}/>

            <GroupSelectedContainer col_span={1} row_span={1}/>
            <Table col_span={3} group={params.group} row_span={2}/>

            <Changes row_span={2}/>

        </svelte:fragment>
    </Row>
