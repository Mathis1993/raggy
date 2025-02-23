<script lang="ts">
    import { Button } from 'flowbite-svelte';
    import { FileOutline } from 'flowbite-svelte-icons';
    import type { MessageSource } from '../types/conversation.js';

    export let source: MessageSource;
    export let isActive: boolean = false;
    export let onClick: () => void;
</script>

<Button
    color="light"
    class="text-sm !p-2 {isActive ? 'ring-2 ring-blue-500' : ''}"
    on:click={onClick}
>
    <div class="flex items-center gap-2">
        <FileOutline class="w-4 h-4" />
        <span class="truncate max-w-[150px]">{source.document.title}</span>
    </div>
</Button> 