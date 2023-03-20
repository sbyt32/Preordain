<script lang="ts">
    import Header from './lib/Header.svelte';
    import Router from 'svelte-spa-router'
    import {routes} from './routes'
    import { projectTitle } from './assets/stores';
</script>


<Header/>

<svelte:head>
    <title>{$projectTitle}</title>
</svelte:head>
<main>
    <div class="container mx-auto pt-2">
        <Router {routes}/>
    </div>
</main>
