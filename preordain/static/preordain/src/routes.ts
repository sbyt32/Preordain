import Groups from "./routes/Groups.svelte";
import Home from "./routes/Home.svelte";
import Inventory from "./routes/Inventory.svelte";
import SearchPage from "./routes/SearchPage.svelte";
import GroupsSelected from "./routes/GroupsSelected.svelte";
import Card from "./routes/Card.svelte";

export const routes = {
    '/': Home,
    '/search/:query?': SearchPage,
    '/inventory/': Inventory,
    '/groups/': Groups,
    '/groups/:group?': GroupsSelected,
    '/card/:set/:cn': Card
}
