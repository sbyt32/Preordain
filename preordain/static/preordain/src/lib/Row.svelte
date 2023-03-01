<script lang="ts">
    export let row_span:number | string = 4
    console.log(row_span);
</script>

<div class="row-span-1">
    <div class="container p-2">
        <span class="inline-grid grid-cols-4 w-full"> <!-- Keep the w-full-->
            <span style="grid-column: span {row_span} / span {row_span}" class="shadow-2xl h-[218px]">
                <slot name="Component">
                    <p class="component-theme empty-space h-full">
                        Place Component Here!
                    </p>
                </slot>
            </span>
        </span>
    </div>
</div>
