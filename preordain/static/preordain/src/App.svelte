<script lang="ts">
    import Header from './lib/Header.svelte';
    import Router from 'svelte-spa-router'
    import {routes} from './routes'
</script>


<Header/>

<main>
    <div class="container mx-auto">
        <Router {routes}/>
    </div>
</main>
