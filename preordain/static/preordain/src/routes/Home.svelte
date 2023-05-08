<script>
    import Row from "../lib/Row.svelte";
    import CardDash from "../lib/CardDash.svelte";
    import PriceGraph from '../lib/charts/PriceGraph.svelte';
    import Changes from '../lib/DailyChanges.svelte';
    import { currentTab, projectTitle } from "../assets/stores";

    projectTitle.set("Home")
    $currentTab = "Home"
</script>

<Row row_span={3} col_span={4}>
    <svelte:fragment slot="Component">
        <div class="col-span-4 row-span-1 component-theme">
            <div class="w-full text-center">
                still in development
            </div>
        </div>
        <CardDash col_span={3} row_span={1}/>
        <Changes/>
        <!-- <PriceGraph col_span={3} row_span={2}/> -->
    </svelte:fragment>
</Row>
