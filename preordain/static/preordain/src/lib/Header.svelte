<script lang="ts">
    import { push } from 'svelte-spa-router';


    // const submit = () => dispatch('submit');

    function onKeyPress(e: KeyboardEvent, str: string) {
        if (e.code === 'Enter') push(`#/search/${str}`);
}

	$:searchQuery = ''

</script>
<div class="bg-gray-500 w-full border-b-2 border-black/20 shadow-lg">
    <div class="grid grid-cols-6">

        <div class="text-center place-self-center text-white">
            Preordain (Testing)
        </div>

        <div class="col-span-4" id="Searchbar">
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

        <div class="place-self-center">
            <button class="component-theme w-fit px-3 py-1 text-base">
                Admin Panel
            </button>
        </div>

    </div>
</div>
