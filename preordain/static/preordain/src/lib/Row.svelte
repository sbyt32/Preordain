<script lang="ts">
    export let row_span:number | string = 2
    // export interface
</script>

<!-- <div class="container mx-auto max-h-[33%] pt-6">
    <div class="grid grid-cols-4 gap-4">
        <span class="col-span-4 inline-grid grid-cols-4 gap-4">
            <span class="col-span-{row_span.toString()}">
                <slot name="Component">Place Component Here!</slot>
            </span>
        </span>
    </div>
</div> -->

<div class="container mx-auto max-h-[25%] pt-6">
    <span class="grid grid-cols-4 gap-4">
        <span class="col-span-{row_span.toString()}">
            <slot name="Component">
                    Place Component Here!
            </slot>
        </span>
    </span>
</div>
