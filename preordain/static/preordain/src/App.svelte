<script lang="ts">
    import Header from './lib/Header.svelte';
    import Router from 'svelte-spa-router'
    import {routes} from './routes'
    import { projectTitle } from './assets/stores';
    import Popup from './assets/Popup.svelte';


</script>
<svelte:head>
    <title>{$projectTitle}</title>
</svelte:head>
<Popup/>

<main class="h-screen max-h-screen">
    <Header/>
    <div class="container mx-auto pt-6 py-4 h-screen">
        <Router {routes}/>
    </div>

</main>
