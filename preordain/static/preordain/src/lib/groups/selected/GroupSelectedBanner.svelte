<script lang="ts">
    export let col_span = 4
    export let row_span = 1
    export let img:string = "https://placekitten.com/g/500/125"
    export let groupName: string = ""
</script>

<div style="grid-column: span {col_span} / span {col_span}; grid-row: span {row_span} / span {row_span};" class=" font-normal min-h-0 h-full w-full relative">
    <div class="absolute font-bold text-xl z-10 w-full h-full">
        <div class="overflow-hidden m-4 h-full content-end inline-flex flex-col text-slate-300/70 gap-1">

            <div class="text-2xl text-white text-left w-full">
                {groupName}
            </div>
            <div class=" text-left w-full hover:text-slate-300 group">
                <p class="w-full">Cards in Group: <span class="text-base group-hover:text-white font-semibold tabular-nums">69420</span></p>
            </div>
            <div class=" text-left w-full hover:text-slate-300 group">
                Last Updated: <span class="text-base group-hover:text-white font-semibold">03/22/2023</span>
            </div>
            <div class=" text-left w-full hover:text-slate-300 group">
                Random: <span class="text-base group-hover:text-white font-semibold">Words</span>
            </div>
            <div class=" text-left w-full hover:text-slate-300 group">
                Stream: <span class="text-base group-hover:text-white font-semibold">All Of The Girls by Taylor Swift</span>
            </div>

        </div>

    </div>
    <img src={img} class="object-cover object-center border border-indigo-600 shadow-amber-600/70 shadow-md h-full w-full select-none opacity-50" alt="sample">
</div>
