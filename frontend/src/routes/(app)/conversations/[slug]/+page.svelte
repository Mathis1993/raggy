<script lang="ts">
    import {Alert, Button, Card, Drawer, Spinner, Textarea, ToolbarButton} from "flowbite-svelte";
    import ChatBubble from "../../../../components/ChatBubble.svelte";
    import {onDestroy, onMount, tick} from "svelte";
    import {createMessage, deleteConversation, getMessages, retrieveConversation, retrieveConversations} from "../conversationService";
    import {goto, invalidateAll} from "$app/navigation";
    import {ChevronLeftSolid, ChevronRightSolid, PapperPlaneOutline} from "flowbite-svelte-icons";
    import {page} from "$app/stores";

    $: conversation = $page.data.conversation;
    $: messages = $page.data.messages.results;
    $: hasMore = $page.data.next !== null;
    $: currentPage = $page.data.page || 1;

    let messageContent = '';
    let chatContainer: HTMLDivElement;
    let rows = 1;
    let refreshIntervalId: number;
    let drawerHidden = false;
    let conversationHistory: any[] = [];
    let historyPage = 1;
    let hasMoreHistory = true;

    $: rows = Math.max(1, messageContent.split('\n').length);

    onMount(async () => {
        scrollToBottom();
        chatContainer.addEventListener('scroll', handleScroll);
        refreshIntervalId = setInterval(refreshDocuments, 5000);
        await loadConversationHistory();
    });

    onDestroy(() => {
        clearInterval(refreshIntervalId);
        chatContainer.removeEventListener('scroll', handleScroll);
    });

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

    function handleKeyDown(event: KeyboardEvent) {
        if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault();
            sendMessage();
        }
    }

    async function sendMessage() {
        let message: string = messageContent;
        messageContent = '';  // clear the input field
        let updatedConversation: Conversation = await createMessage(message, conversation);
        conversation = updatedConversation
        messages = updatedConversation.messages
        await tick(); // wait for the new message to be rendered
        scrollToBottom(); // scroll to the bottom
        await invalidateAll();
        await refreshDocuments(); // start the refresh logic
    }

    function scrollToBottom() {
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    async function refreshDocuments() {
        if (conversation.status === 'RUNNING') {
            conversation = await retrieveConversation(conversation.id);
            messages = conversation.messages;
            await tick(); // wait for the new message to be rendered
            scrollToBottom();
        }
    }

    async function loadMoreMessages() {
        currentPage++;
        // Compute scroll position before loading more messages
        const oldScrollHeight = chatContainer.scrollHeight; // get the old scroll height
        const oldScrollTop = chatContainer.scrollTop; // get the old scroll position

        const newMessages = await getMessages(conversation.id, currentPage);
        messages = [...newMessages.results, ...messages];

        await tick(); // wait for the new messages to be rendered
        const newScrollHeight = chatContainer.scrollHeight; // get the new scroll height
        chatContainer.scrollTop = oldScrollTop + (newScrollHeight - oldScrollHeight); // adjust the scroll position
    }

    function handleScroll() {
        if (chatContainer.scrollTop === 0) { // if the scroll position is at the top
            loadMoreMessages(); // load more messages
        }
    }

</script>

<div class="flex h-full relative">
    <div class="flex-1 max-w-full flex-grow flex-col h-full max-h-[calc(100vh-12vh)]">
        <Card class="max-w-full h-full shadow-0">
            <div class="flex justify-between items-center mb-4">
                <h5 class="text-2xl font-bold tracking-tight text-gray-900 dark:text-white">
                    {conversation.name || "Start Conversation..."}
                </h5>
                <button on:click={() => deleteConversation(conversation.id)} class="text-white m-0">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
                         stroke="currentColor" class="h-6 w-6 text-red-500 hover:text-red-700">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                              d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                    </svg>
                </button>
            </div>
            <div class="max-w-full h-[calc(100vh-35vh)] flex-grow overflow-auto" bind:this={chatContainer}>
                {#each messages as message}
                    <ChatBubble {message}/>
                {/each}
                {#if conversation.status === 'RUNNING'}
                    <div class="flex items-center justify-center">
                        <Spinner/>
                    </div>
                {/if}
            </div>

            <form class="mt-4" on:submit|preventDefault={() => sendMessage()}>
                <label for="chat" class="sr-only">Your message</label>
                <Alert color="dark" class="px-3 py-2">
                    <svelte:fragment slot="icon">
                        <Textarea id="message" class="mx-4 text-lg" {rows} placeholder="Your message..."
                                 bind:value={messageContent}
                                 on:keydown={handleKeyDown}/>
                        <ToolbarButton type="submit" color="blue"
                                      class="rounded-full text-primary-600 dark:text-primary-500">
                            <PapperPlaneOutline class="w-5 h-5 rotate-45"/>
                            <span class="sr-only">Send message</span>
                        </ToolbarButton>
                    </svelte:fragment>
                </Alert>
            </form>
        </Card>
    </div>

    <!-- History Toggle Button -->
    <button
        class="absolute right-0 top-1/2 transform -translate-y-1/2 translate-x-1/2 z-10 bg-gray-800 dark:bg-gray-700 text-white rounded-full p-3 shadow-xl hover:bg-gray-700 dark:hover:bg-gray-600 transition-all duration-200 border-2 border-gray-700 dark:border-gray-600"
        on:click={toggleHistory}
    >
        {#if !drawerHidden}
            <ChevronRightSolid class="w-5 h-5"/>
        {:else}
            <ChevronLeftSolid class="w-5 h-5"/>
        {/if}
    </button>

    <!-- History Sidebar -->
    <Drawer
        placement="right"
        width="w-80"
        class="p-4 bg-white dark:bg-gray-800 border-l border-gray-200 dark:border-gray-700"
        transitionType="fly"
        hidden={drawerHidden}
    >
        <div class="h-full overflow-y-auto">
            <h5 class="mb-4 text-xl font-bold text-gray-900 dark:text-white">Chat History</h5>
            {#if conversationHistory.length === 0}
                <p class="text-gray-500 dark:text-gray-400">No conversations yet</p>
            {:else}
                <div class="space-y-2">
                    {#each conversationHistory as conv}
                        <div
                            class="p-3 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 cursor-pointer {conv.id === conversation.id ? 'bg-gray-100 dark:bg-gray-700' : ''}"
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
                {#if hasMoreHistory}
                    <Button class="w-full mt-4" color="light" on:click={loadMoreHistory}>
                        Load More
                    </Button>
                {/if}
            {/if}
        </div>
    </Drawer>
</div>