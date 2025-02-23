<script lang="ts">
    export let onMouseDown: (e: MouseEvent) => void;
</script>

<div
    class="absolute left-0 top-0 w-1 h-full cursor-col-resize group hover:bg-blue-500/20 active:bg-blue-500/40"
    on:mousedown={onMouseDown}
>
    <div class="absolute left-0 top-0 w-4 h-full -translate-x-1/2">
        <div class="absolute left-1/2 top-1/2 -translate-y-1/2 w-1 h-8 rounded-full bg-gray-300 dark:bg-gray-600 opacity-0 group-hover:opacity-100 group-active:opacity-100 transition-opacity"></div>
    </div>
</div> 