<script lang="ts">
    export let col_span:number | string = 4
    export let row_span:number | string = 3

    console.log(col_span);
</script>

<div class="flex flex-col h-full">
    <div class="inline-grid gap-4 h-[90vh]" style="grid-template-columns: repeat({col_span}, minmax(0, 1fr)); grid-template-rows: repeat({row_span}, minmax(0, 1fr));">
        <slot name="Component">
            <p class="component-theme empty-space col-span-1 row-span-1">
                Place Component Here!
            </p>
        </slot>
    </div>
</div>
