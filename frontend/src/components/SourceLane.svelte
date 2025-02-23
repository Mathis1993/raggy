<script lang="ts">
    import { Button } from 'flowbite-svelte';
    import { CloseOutline } from 'flowbite-svelte-icons';
    import type { MessageSource } from '../types/conversation.js';
    import ResizeHandle from './ResizeHandle.svelte';
    import { onMount } from 'svelte';

    export let selectedSource: MessageSource | null = null;
    export let onClose: () => void;
    export let width = 384; // 24rem (w-96)

    let isDragging = false;
    let startX: number;
    let startWidth: number;
    let container: HTMLDivElement;

    $: documentTitle = selectedSource?.document?.title || 'Source';
    $: clampedWidth = Math.min(Math.max(width, 320), window.innerWidth / 2); // min 320px, max 50% of window

    function handleMouseDown(event: MouseEvent) {
        isDragging = true;
        startX = event.pageX;
        startWidth = width;
        
        // Add event listeners to window to handle dragging
        window.addEventListener('mousemove', handleMouseMove);
        window.addEventListener('mouseup', handleMouseUp);
        
        // Add a class to prevent text selection while dragging
        document.body.classList.add('select-none');
    }

    function handleMouseMove(event: MouseEvent) {
        if (!isDragging) return;
        const diff = startX - event.pageX;
        width = Math.min(Math.max(startWidth + diff, 320), window.innerWidth / 2);
    }

    function handleMouseUp() {
        isDragging = false;
        window.removeEventListener('mousemove', handleMouseMove);
        window.removeEventListener('mouseup', handleMouseUp);
        document.body.classList.remove('select-none');
    }

    onMount(() => {
        return () => {
            window.removeEventListener('mousemove', handleMouseMove);
            window.removeEventListener('mouseup', handleMouseUp);
        };
    });
</script>

<div 
    bind:this={container}
    class="h-full bg-white dark:bg-gray-800 border-l border-gray-200 dark:border-gray-700 flex flex-col relative"
    style="width: {clampedWidth}px"
>
    <ResizeHandle onMouseDown={handleMouseDown} />
    
    <div class="p-4 border-b border-gray-200 dark:border-gray-700 flex justify-between items-center">
        <h2 class="text-lg font-semibold text-gray-900 dark:text-white">{documentTitle}</h2>
        <Button color="light" class="!p-2" on:click={onClose}>
            <CloseOutline class="w-4 h-4"/>
        </Button>
    </div>
    
    {#if selectedSource}
        <div class="flex-1 p-4 overflow-y-auto">
            <div class="prose dark:prose-invert max-w-none">
                <div class="bg-gray-50 dark:bg-gray-900 p-4 rounded-lg">
                    <p class="text-gray-700 dark:text-gray-300">
                        {#if selectedSource.content}
                            {@html selectedSource.content.slice(0, selectedSource.highlighted_content.start)}
                            <span class="bg-yellow-100 dark:bg-yellow-900">
                                {@html selectedSource.content.slice(
                                    selectedSource.highlighted_content.start,
                                    selectedSource.highlighted_content.end
                                )}
                            </span>
                            {@html selectedSource.content.slice(selectedSource.highlighted_content.end)}
                        {/if}
                    </p>
                </div>
                
                {#if selectedSource.document}
                    <div class="mt-4">
                        <h3 class="text-sm font-medium text-gray-500 dark:text-gray-400">Source Details</h3>
                        <dl class="mt-2 text-sm">
                            <div class="mt-1">
                                <dt class="text-gray-500 dark:text-gray-400">Document</dt>
                                <dd class="text-gray-900 dark:text-white">{selectedSource.document.title}</dd>
                            </div>
                        </dl>
                    </div>
                {/if}
            </div>
        </div>
    {:else}
        <div class="flex-1 flex items-center justify-center">
            <p class="text-gray-500 dark:text-gray-400">Select a source to view details</p>
        </div>
    {/if}
</div>

<style>
    /* Add a style to prevent text selection while dragging */
    :global(body.select-none) {
        user-select: none;
    }
</style> 