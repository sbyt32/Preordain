<script lang="ts">
    export let col_span = 1
    export let row_span = 1
</script>

<div style="grid-column: span {col_span} / span {col_span}; grid-row: span {row_span} / span {row_span};" class="p-2 font-normal component-theme flex flex-col">
    <img src="https://placekitten.com/g/500/125" class="object-scale-down self-center border rounded-xl border-indigo-600 shadow-amber-600/80 shadow-md" height="150px" width="500px" alt="sample">

    <br>
    <!-- Information -->
    <div class="text-base grow">
        <p class="text-ellipsis overflow-hidden whitespace-nowrap">Cards in Group: <span class="italic text-sm">69420</span></p>
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
