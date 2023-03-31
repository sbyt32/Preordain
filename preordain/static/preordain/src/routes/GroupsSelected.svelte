<script lang="ts">
    import Row from "../lib/Row.svelte";
    import CardDash from "../lib/CardDash.svelte";
    import Changes from '../lib/DailyChanges.svelte';
    import Table from '../lib/groups/Table.svelte';
    import GroupSelectedContainer from "../lib/groups/selected/GroupSelectedContainer.svelte";
    import GroupSelectedBanner from "../lib/groups/selected/GroupSelectedBanner.svelte";
    import { connectURL, projectTitle } from "../assets/stores";
    import testThalia from '/test_thalia.jpg';
    import { database } from "../util/fetch_data";


    export let params = {group: ""}

    projectTitle.set(`Group: ${params.group}`)

</script>


{#await database(`${$connectURL}/groups/${params.group}`) then groupData}
    <Row row_span={4} col_span={4}>
        <svelte:fragment slot="Component">
            <GroupSelectedBanner img={testThalia} groupInfo={groupData.info}/>
            <CardDash col_span={3} row_span={1}/>

            <GroupSelectedContainer col_span={1} row_span={1}/>
            <Table col_span={3} row_span={2} groupData={groupData}/>
            <Changes col_span={1}/>


        </svelte:fragment>
    </Row>
{/await}
