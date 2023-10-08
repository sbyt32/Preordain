// import SearchPage from "./src/routes/SearchPage.svelte";
import SearchPage from "./src/routes/search_page/SearchPage.svelte"
import CardPage from "./src/routes/card_page/CardPage.svelte"

export const routes = {
    "/search/:query": SearchPage,
    "/card/:set/:id": CardPage
}
