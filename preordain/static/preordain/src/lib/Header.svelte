<script lang="ts">
  import AdminPanel from './header/AdminPanel.svelte';
  import icon from "/favicon.ico"
  import HomeMenu from './header/HomePanel.svelte';

    import { push } from 'svelte-spa-router';



    function onKeyPress(e: KeyboardEvent, str: string) {
        if (e.code === 'Enter') push(`#/search/${str}`);
}

	$:searchQuery = ''
    $:dropdown = false
</script>
<div class="bg-gray-500 w-full border-b-2 border-black/20 shadow-lg mb-2">
    <div class="flex flex-row gap-20 first:ml-20 last:mr-20 py-1">

        {icon}
        <HomeMenu/>

        <div class="grow" id="Searchbar">
            <form class="items-center">
                <label for="simple-search" class="sr-only">Search</label>
                <div class="relative w-full">
                    <div class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
                        <svg aria-hidden="true" class="w-5 h-5 text-gray-500 dark:text-gray-400" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clip-rule="evenodd"></path></svg>
                    </div>
                    <input
                        type="text"
                        class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg
                            focus:ring-blue-500 focus:border-blue-500 block w-full pl-10 p-2.5
                            dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white
                            dark:focus:ring-blue-500 dark:focus:border-blue-500"
                            bind:value={searchQuery}
                            on:keydown={(event) => onKeyPress(event, searchQuery)}
                    >
                </div>
            </form>
        </div>

        <AdminPanel/>

    </div>
</div>
