<script lang="ts">
    export let col_span = 1
    export let row_span = 1
    // export let img:string = "https://placekitten.com/g/500/125"
</script>

<div style="grid-column: span {col_span} / span {col_span}; grid-row: span {row_span} / span {row_span};" class="p-2 font-normal component-theme flex flex-col">
    <h1 class="text-center border-b-2 border-b-gray-700">
        At a Glance:
    </h1>
    <br>
    <!-- Information -->
    <div class="text-base grow">
        <p class="text-ellipsis overflow-hidden whitespace-nowrap">📈 🇺🇸: <span class="italic text-sm">Thalia, Guardian of Thraben <span class="tabular-nums">($0.66)</span></span></p>
        <p class="text-ellipsis overflow-hidden whitespace-nowrap">📈 🇪🇺: <span class="italic text-sm">Thalia, Guardian of Thraben <span class="tabular-nums">($0.66)</span></span></p>
        <p class="text-ellipsis overflow-hidden whitespace-nowrap">📉 🇺🇸: <span class="italic text-sm">Thalia, Guardian of Thraben <span class="tabular-nums">($0.66)</span></span></p>
        <p class="text-ellipsis overflow-hidden whitespace-nowrap">📉 🇪🇺: <span class="italic text-sm">Thalia, Guardian of Thraben <span class="tabular-nums">($0.66)</span></span></p>

    </div>

    <div class="text-center">
        <button class="preordain-button">
            Add Cards
        </button>
        <button class="preordain-button delete">
            Remove Cards
        </button>
    </div>
</div>
