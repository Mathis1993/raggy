<script lang="ts">
    import { Button } from 'flowbite-svelte';
    import { ChevronLeftSolid, ChevronRightSolid } from 'flowbite-svelte-icons';
    import { goto } from '$app/navigation';
    import { onMount } from 'svelte';
    import { retrieveConversations } from '../routes/(app)/conversations/conversationService';

    export let currentConversationId: number | null = null;
    
    let drawerHidden = true;
    let conversationHistory: any[] = [];
    let historyPage = 1;
    let hasMoreHistory = true;

    async function loadConversationHistory() {
        const response = await retrieveConversations(historyPage);
        if (response.results) {
            conversationHistory = [...conversationHistory, ...response.results];
            hasMoreHistory = response.next !== null;
            historyPage = response.page;
        }
    }

    async function loadMoreHistory() {
        if (!hasMoreHistory) return;
        historyPage++;
        await loadConversationHistory();
    }

    function toggleHistory() {
        drawerHidden = !drawerHidden;
    }

    async function navigateToConversation(id: number) {
        drawerHidden = true; // Close the drawer when selecting a conversation
        await goto(`/conversations/${id}`);
    }

    // Load history when component mounts
    onMount(() => {
        loadConversationHistory();
    });
</script>

<!-- History Toggle Button -->
<button
    class="fixed right-0 top-1/2 transform -translate-y-1/2 translate-x-[25%] z-20 bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-300 rounded-full p-2.5 shadow-lg hover:bg-gray-200 dark:hover:bg-gray-700 transition-all duration-200 border border-gray-200 dark:border-gray-700"
    on:click={toggleHistory}
>
    {#if !drawerHidden}
        <ChevronRightSolid class="w-5 h-5"/>
    {:else}
        <ChevronLeftSolid class="w-5 h-5"/>
    {/if}
</button>

<!-- History Sidebar -->
<div class="fixed right-0 top-16 bottom-0 w-80 transition-transform duration-200 z-10"
     class:translate-x-full={drawerHidden}>
    <div class="h-full bg-white dark:bg-gray-800 border-l border-gray-200 dark:border-gray-700 flex flex-col">
        <div class="p-4 border-b dark:border-gray-700">
            <h5 class="text-lg font-semibold text-gray-900 dark:text-white">Chat History</h5>
        </div>
        <div class="flex-1 overflow-y-auto p-4">
            {#if conversationHistory.length === 0}
                <p class="text-gray-500 dark:text-gray-400">No conversations yet</p>
            {:else}
                <div class="space-y-2">
                    {#each conversationHistory as conv}
                        <div
                            class="p-3 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 cursor-pointer {conv.id === currentConversationId ? 'bg-gray-100 dark:bg-gray-700' : ''}"
                            on:click={() => navigateToConversation(conv.id)}
                        >
                            <h6 class="text-sm font-medium text-gray-900 dark:text-white">
                                {conv.name || "Untitled Chat"}
                            </h6>
                            <p class="text-xs text-gray-500 dark:text-gray-400">
                                {new Date(conv.created_at).toLocaleDateString()}
                            </p>
                        </div>
                    {/each}
                </div>
            {/if}
        </div>
        {#if hasMoreHistory}
            <div class="p-4 border-t dark:border-gray-700">
                <Button class="w-full" color="light" on:click={loadMoreHistory}>
                    Load More
                </Button>
            </div>
        {/if}
    </div>
</div>

<style>
    /* Add margin to main content when drawer is open */
    :global(.content-wrapper) {
        transition: all 0.2s ease-in-out;
        margin: 0 auto;
    }
    :global(.content-wrapper.drawer-open) {
        margin-right: 20rem;
        margin-left: -10rem; /* Move content to the left when drawer opens */
    }
</style> 