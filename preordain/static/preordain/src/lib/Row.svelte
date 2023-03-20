<script lang="ts">
    export let col_span:number | string = 5
    console.log(col_span);
</script>

    <span class="inline-grid grid-cols-4 grid-rows-3 gap-4">
        <slot name="Component">
            <p class="component-theme empty-space col-span-1 row-span-1">
                Place Component Here!
            </p>
        </slot>
    </span>
