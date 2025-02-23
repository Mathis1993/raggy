<script lang="ts">
    import markdownit from 'markdown-it';
    import type { Message, MessageSource } from '../types/conversation.js';
    import SourceButton from './SourceButton.svelte';

    export let message: Message;
    export let onSourceClick = (source: MessageSource) => {};

    const md = markdownit({
        html: true,
        linkify: true,
        typographer: true
    });
    $: html = md.render(message.text);
</script>

<div class="flex gap-3 mb-6">
    <div class="w-8 h-8 flex-shrink-0 rounded-full bg-gray-200 dark:bg-gray-700 flex items-center justify-center text-gray-600 dark:text-gray-300 mt-1">
        {message.is_user_message ? 'T' : 'A'}
    </div>
    
    <div class="flex-1 max-w-[85%]">
        <div class="rounded-lg px-4 py-3 {message.is_user_message ? 'bg-blue-600 text-white' : 'bg-white dark:bg-gray-800 text-gray-900 dark:text-white'}">
            <div class="prose dark:prose-invert max-w-none {message.is_user_message ? 'prose-white' : ''}">
                {@html html}
            </div>
            
            {#if !message.is_user_message && message.sources && message.sources.length > 0}
                <div class="flex gap-2 mt-3 pt-3 border-t border-gray-200 dark:border-gray-700">
                    {#each message.sources as source}
                        <SourceButton
                            {source}
                            onClick={() => onSourceClick(source)}
                        />
                    {/each}
                </div>
            {/if}
        </div>
    </div>
</div>

<style>
    /* Style overrides for white text in user messages */
    :global(.prose-white) {
        color: white;
    }
    :global(.prose-white strong) {
        color: white;
    }
    :global(.prose-white a) {
        color: white;
        text-decoration: underline;
    }
    :global(.prose-white p) {
        color: white;
        margin: 0;
    }
    :global(.prose p) {
        margin: 0;
    }
</style>
