<script lang="ts">
    import {Alert, Button, Card, Spinner, Textarea, ToolbarButton} from "flowbite-svelte";
    import ChatBubble from "../../../../components/ChatBubble.svelte";
    import ConversationHistory from "../../../../components/ConversationHistory.svelte";
    import {onDestroy, onMount, tick} from "svelte";
    import {createMessage, deleteConversation, getMessages, retrieveConversation} from "../conversationService";
    import {goto, invalidateAll} from "$app/navigation";
    import {PapperPlaneOutline} from "flowbite-svelte-icons";
    import {page} from "$app/stores";
    import type { MessageSource, Conversation, Message } from '../../../../types/conversation.js';
    import SourceLane from '../../../../components/SourceLane.svelte';
    import TypingIndicator from '../../../../components/TypingIndicator.svelte';
    import { slide } from 'svelte/transition';

    $: conversation = $page.data.conversation;
    $: messages = conversation?.messages || [];
    $: hasMore = $page.data.next !== null;
    $: currentPage = $page.data.page || 1;
    $: isTyping = conversation?.status === 'RUNNING';
    $: if (isTyping) {
        tick().then(() => scrollToBottom());
    }

    let messageContent = '';
    let rows = 1;
    let refreshIntervalId: number;
    let selectedSource: MessageSource | null = null;
    let isSourceLaneOpen = false;
    let sourceLaneWidth = 384;

    // Update CSS variable when width changes
    $: if (typeof document !== 'undefined') {
        document.documentElement.style.setProperty('--source-lane-width', `${sourceLaneWidth}px`);
    }

    $: rows = Math.max(1, messageContent.split('\n').length);

    let messageContainer: HTMLDivElement;

    onMount(() => {
        scrollToBottom();
        messageContainer?.addEventListener('scroll', handleScroll);
        refreshIntervalId = setInterval(refreshDocuments, 5000);
    });

    onDestroy(() => {
        if (refreshIntervalId) {
            clearInterval(refreshIntervalId);
        }
        messageContainer?.removeEventListener('scroll', handleScroll);
    });

    function handleKeyDown(event: KeyboardEvent) {
        if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault();
            handleSubmit();
        }
    }

    async function handleSubmit() {
        if (!messageContent.trim()) return;
        const currentMessage = messageContent;
        messageContent = '';
        
        const response = await createMessage(currentMessage, conversation);
        if (response) {
            conversation = response;
            messages = response.messages;
            await tick();
            scrollToBottom();
        }
    }

    function scrollToBottom() {
        if (messageContainer) {
            messageContainer.scrollTop = messageContainer.scrollHeight;
        }
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
        if (messageContainer?.scrollTop === 0) { // if the scroll position is at the top
            loadMoreMessages(); // load more messages
        }
    }

    async function loadMoreMessages() {
        if (!messageContainer) return;
        
        currentPage++;
        // Compute scroll position before loading more messages
        const oldScrollHeight = messageContainer.scrollHeight;
        const oldScrollTop = messageContainer.scrollTop;

        const newMessages = await getMessages(conversation.id, currentPage);
        messages = [...newMessages.results, ...messages];

        await tick(); // wait for the new messages to be rendered
        const newScrollHeight = messageContainer.scrollHeight;
        messageContainer.scrollTop = oldScrollTop + (newScrollHeight - oldScrollHeight);
    }

    function handleSourceClick(source: MessageSource) {
        selectedSource = source;
        isSourceLaneOpen = true;
    }

    function closeSourceLane() {
        isSourceLaneOpen = false;
        selectedSource = null;
    }
</script>

<div class="flex h-[calc(100vh-4rem)] relative bg-gray-50 dark:bg-gray-900">
    <div class="flex-1 flex overflow-hidden">
        <div class="flex-1 flex justify-center">
            <div 
                class="w-full max-w-3xl flex flex-col relative px-4" 
                style="
                    margin-right: {isSourceLaneOpen ? 'var(--source-lane-width, 384px)' : 'auto'}; 
                    margin-left: {isSourceLaneOpen ? '0' : 'auto'};
                    transition: margin 300ms ease-in-out;
                "
            >
                <div class="flex-1 overflow-y-auto py-4" bind:this={messageContainer}>
                    <div class="space-y-4">
                        {#each messages as message}
                            <ChatBubble 
                                {message} 
                                onSourceClick={handleSourceClick}
                            />
                        {/each}
                        {#if isTyping}
                            <div transition:slide|local={{ duration: 200 }}>
                                <TypingIndicator />
                            </div>
                        {/if}
                    </div>
                </div>

                <div class="sticky bottom-0 bg-gray-50 dark:bg-gray-900 py-4">
                    <form on:submit|preventDefault={handleSubmit} class="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-4">
                        <div class="flex items-stretch gap-4">
                            <div class="flex-1">
                                <Textarea
                                    id="message"
                                    class="w-full resize-none rounded-lg border border-gray-200 dark:border-gray-600 bg-white dark:bg-gray-700 px-4 py-2.5"
                                    rows={rows}
                                    maxRows={10}
                                    placeholder="Type your message..."
                                    bind:value={messageContent}
                                    on:keydown={handleKeyDown}
                                />
                            </div>
                            <div class="flex">
                                <Button type="submit" color="blue" class="px-6 !h-[42px]" disabled={!messageContent.trim()}>
                                    <PapperPlaneOutline class="w-4 h-4 rotate-45"/>
                                </Button>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>

    <ConversationHistory currentConversationId={conversation.id} />

    {#if isSourceLaneOpen}
        <div class="fixed right-0 h-[calc(100vh-4rem)]" transition:slide|local={{ duration: 300, axis: 'x' }}>
            <SourceLane
                {selectedSource}
                onClose={closeSourceLane}
                bind:width={sourceLaneWidth}
            />
        </div>
    {/if}
</div>

<style>
    :root {
        --source-lane-width: 384px;
    }

    :global(textarea) {
        min-height: 44px;
        max-height: 300px;
    }
</style>