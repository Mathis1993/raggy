<script lang="ts">
    import {Alert, Button, Card, Spinner, Textarea, ToolbarButton} from "flowbite-svelte";
    import ChatBubble from "../../../../components/ChatBubble.svelte";
    import ConversationHistory from "../../../../components/ConversationHistory.svelte";
    import {onDestroy, onMount, tick} from "svelte";
    import {createMessage, deleteConversation, getMessages, retrieveConversation} from "../conversationService";
    import {goto, invalidateAll} from "$app/navigation";
    import {PapperPlaneOutline} from "flowbite-svelte-icons";
    import {page} from "$app/stores";

    $: conversation = $page.data.conversation;
    $: messages = $page.data.messages.results;
    $: hasMore = $page.data.next !== null;
    $: currentPage = $page.data.page || 1;

    let messageContent = '';
    let chatContainer: HTMLDivElement;
    let rows = 1;
    let refreshIntervalId: number;

    $: rows = Math.max(1, messageContent.split('\n').length);

    onMount(async () => {
        scrollToBottom();
        chatContainer.addEventListener('scroll', handleScroll);
        refreshIntervalId = setInterval(refreshDocuments, 5000);
    });

    onDestroy(() => {
        clearInterval(refreshIntervalId);
        chatContainer.removeEventListener('scroll', handleScroll);
    });

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

    function handleScroll() {
        if (chatContainer.scrollTop === 0) { // if the scroll position is at the top
            loadMoreMessages(); // load more messages
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

</script>

<div class="flex h-[calc(100vh-4rem)] relative bg-gray-50 dark:bg-gray-900 overflow-hidden">
    <!-- Main Chat Container -->
    <div class="flex-1 flex justify-center w-full content-wrapper">
        <!-- Main Chat Area with max width and padding -->
        <div class="flex flex-col h-full w-full max-w-4xl px-6">
            <!-- Chat Header -->
            <div class="flex justify-between items-center py-6 border-b dark:border-gray-700">
                <h5 class="text-xl font-semibold text-gray-900 dark:text-white flex items-center gap-2">
                    <span>{conversation.name || "New Conversation"}</span>
                    {#if conversation.status === 'RUNNING'}
                        <Spinner size="4" class="ml-2"/>
                    {/if}
                </h5>
                <button on:click={() => deleteConversation(conversation.id)} 
                        class="text-gray-500 hover:text-red-600 transition-colors">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
                         stroke="currentColor" class="h-5 w-5">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                              d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                    </svg>
                </button>
            </div>

            <!-- Chat Messages -->
            <div class="flex-1 overflow-y-auto py-6 space-y-6" bind:this={chatContainer}>
                <div class="space-y-6">
                    {#each messages as message}
                        <ChatBubble {message}/>
                    {/each}
                </div>
            </div>

            <!-- Chat Input -->
            <div class="border-t dark:border-gray-700 py-6">
                <form on:submit|preventDefault={() => sendMessage()} class="flex gap-3">
                    <div class="flex-1 relative">
                        <Textarea
                            id="message"
                            class="w-full resize-none rounded-lg border border-gray-200 dark:border-gray-600 bg-white dark:bg-gray-700 px-4 py-3"
                            {rows}
                            placeholder="Type your message..."
                            bind:value={messageContent}
                            on:keydown={handleKeyDown}
                        />
                    </div>
                    <Button type="submit" color="blue" class="px-4 self-end">
                        <PapperPlaneOutline class="w-5 h-5 rotate-45"/>
                        <span class="sr-only">Send message</span>
                    </Button>
                </form>
            </div>
        </div>
    </div>

    <ConversationHistory currentConversationId={conversation.id} />
</div>