import Home from "./routes/Home.svelte";
import SearchPage from "./routes/SearchPage.svelte";

export const routes = {
    '/': Home,
    '/search/:query': SearchPage,
}
