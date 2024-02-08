<script lang="ts">
    import {Alert, Card, Spinner, Textarea, ToolbarButton} from "flowbite-svelte";
    import ChatBubble from "../../../components/ChatBubble.svelte";
    import {onDestroy, onMount, tick} from "svelte";
    import {createMessage, deleteConversation, retrieveConversation} from "../conversationService";
    import {invalidateAll} from "$app/navigation";
    import {PapperPlaneOutline} from "flowbite-svelte-icons";
    import {retrieveDocument} from "../../documents/documentService";

    export let data;
    let conversation = data.conversation;
    let messages: Message[] = data.conversation.messages;
    let messageContent = '';
    let chatContainer: HTMLDivElement;

    onMount(() => {
        scrollToBottom();
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
        let updatedConversation: Conversation = await createMessage(message, data.conversation);
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

    let refreshIntervalId: number;
    onMount(() => {
        refreshIntervalId = setInterval(refreshDocuments, 5000);
    });

    onDestroy(() => {
        // Clear the interval when the component is destroyed
        clearInterval(refreshIntervalId);
    });

    async function refreshDocuments() {
        if (conversation.status === 'RUNNING') {
            conversation = await retrieveConversation(conversation.id);
            messages = conversation.messages;
            await tick(); // wait for the new message to be rendered
            scrollToBottom();
        }
    }

</script>


<div class="flex max-w-full flex-grow flex-col h-full">
    <Card class="max-w-full h-full shadow-0">
        <div class="flex justify-between items-center mb-4 ">
            <h5 class="text-2xl font-bold tracking-tight text-gray-900 dark:text-white"> {conversation.name || "Start Conversation..."}</h5>
            <button on:click={() => deleteConversation(conversation.id)} class="text-white m-0">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
                     stroke="currentColor" class="h-6 w-6 text-red-500 hover:text-red-700">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                          d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
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
                    <Textarea id="message" class="mx-4 text-md" rows="1" placeholder="Your message..."
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
