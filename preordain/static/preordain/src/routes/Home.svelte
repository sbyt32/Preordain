<script>
    import Row from "../lib/Row.svelte";
    import CardDash from "../lib/CardDash.svelte";
    import PriceGraph from '../lib/charts/PriceGraph.svelte';
    import Changes from '../lib/DailyChanges.svelte';
    import { projectTitle } from "../assets/stores";

    projectTitle.set("Home")
</script>

    <Row>
        <svelte:fragment slot="Component">
            <CardDash col_span=3/>
            <Changes col_span=1/>
            <PriceGraph col_span=3/>
        </svelte:fragment>
    </Row>
