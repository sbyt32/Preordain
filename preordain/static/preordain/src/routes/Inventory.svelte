<script>
    import { currentTab, projectTitle } from "../assets/stores";
    import AddInventory from '../lib/inventory/AddInventory.svelte';
    import DisplayInventory from '../lib/inventory/DisplayInventory.svelte';
    import Row from '../lib/Row.svelte';

    projectTitle.set("Inventory")
    $currentTab = "Inventory"
</script>

<Row col_span={4} row_span={5}>
    <svelte:fragment slot="Component">
        <AddInventory row_span={1}/>

        <DisplayInventory row_span={3} col_span={4}/>
    </svelte:fragment>
</Row>
