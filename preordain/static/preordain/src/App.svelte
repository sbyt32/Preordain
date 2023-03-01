<script lang="ts">
    import CardDash from './lib/CardDash.svelte';
    import Table from './lib/Table.svelte';
    import Row from './lib/Row.svelte';
    import Header from './lib/Header.svelte';
    import PriceGraph from './lib/charts/PriceGraph.svelte';
</script>



<main class="h-full">
    <Header/>
    <div class="container mx-auto">

        <div class="grid grid-cols-1 grid-rows-4 content-evenly">
            <Row row_span=3>
                <svelte:fragment slot="Component">
                    <CardDash/>
                </svelte:fragment>
            </Row>

            <Row row_span=4>
                <svelte:fragment slot="Component">
                    <Table/>
                </svelte:fragment>
            </Row>
            <Row>
                <svelte:fragment slot="Component">
                    <PriceGraph/>
                </svelte:fragment>
            </Row>

            <Row>
            <svelte:fragment slot="Component">
            </svelte:fragment>
            </Row>


        </div>
    </div>

</main>
