// import SearchPage from "./src/routes/SearchPage.svelte";
import SearchPage from "./src/routes/search_page/SearchPage.svelte"
import CardPage from "./src/routes/card_page/CardPage.svelte"
import { wrap } from "svelte-spa-router/wrap"

// https://github.com/ItalyPaleAle/svelte-spa-router/blob/master/Advanced%20Usage.md#route-pre-conditions
export const routes = {
    "/search/:query": SearchPage,
    "/card/:set/:id": CardPage
}
