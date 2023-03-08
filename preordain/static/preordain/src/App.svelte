<script lang="ts">
    import CardDash from './lib/CardDash.svelte';
    import Table from './lib/Table.svelte';
    import Row from './lib/Row.svelte';
    import Header from './lib/Header.svelte';
    import PriceGraph from './lib/charts/PriceGraph.svelte';
    import Changes from './lib/Changes.svelte';
</script>



<main>
    <Header/>
    <div class="container mx-auto">
        <div class="grid grid-cols-4 grid-rows-4 h-2/3">
            <Row>
                <svelte:fragment slot="Component">
                    <CardDash col_span=3/>
                    <Changes col_span=1/>
                    <Table col_span=3/>
                </svelte:fragment>
            </Row>
            <Row>
                <svelte:fragment slot="Component">
                    <PriceGraph col_span=3/>
                </svelte:fragment>
            </Row>

        </div>
    </div>

</main>
