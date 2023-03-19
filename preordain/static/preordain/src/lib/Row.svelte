<script lang="ts">
    export let col_span:number | string = 4
    console.log(col_span);
</script>

<div class="row-span-4 col-span-4 p-2">
    <span class="inline-grid grid-cols-4 w-full h-full gap-3">
        <slot name="Component">
            <p class="component-theme empty-space h-full">
                Place Component Here!
            </p>
        </slot>
    </span>
</div>
