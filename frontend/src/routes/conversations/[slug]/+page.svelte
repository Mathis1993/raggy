<script lang="ts">
    import {Card} from "flowbite-svelte";
    import ChatBubble from "../../../components/ChatBubble.svelte";
    import { page } from '$app/stores';
    import {onMount} from "svelte";
    import {goto, invalidateAll} from "$app/navigation";

    export let data;
    let conversation: Conversation = data.conversation;
    let messages: Message[] = data.conversation.messages;
    let messageContent = '';

    // auto scroll to bottom
    let chatContainer: ChatBubble;
    onMount(() => {
        chatContainer.scrollTop = chatContainer.scrollHeight;
    });

    async function createMessage(messageText: string) {
        const message = messageText.trim();
        messageContent = ''; // Clear the textarea after sending the message
        // TODO: replace this when its an async process in the backend which returns the message with the id
        messages = [...messages, {
            id: messages.length + 1,
            text: message,
            conversation: conversation,
            is_user_message: true,
            created_at: new Date().toISOString(),
        }];
        chatContainer.scrollTop = chatContainer.scrollHeight;

        const response = await fetch('http://localhost:8000/api/conversations/' + conversation.id + "/messages/", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({"message": message, "conversation_id": conversation.id}),
        });

        if (!response.ok) {
            console.error('Failed to send message', response);
            return;
        }
        // reload the conversation to get the new message
        await invalidateAll()
        messages = data.conversation.messages;
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    async function deleteConversation(id: number) {
        try {
            const response = await fetch("http://localhost:8000/api/conversations/" + conversation.id, {
                method: 'DELETE',
            });

            if (!response.ok) {
                console.error('Failed to delete conversation');
                return;
            }

            console.log('Conversation deleted');
        } catch (error) {
            console.error('Failed to delete conversation', error);
        }
        console.log('Redirecting to /conversations/');
        await goto(`/conversations/`, {replaceState: true});
        await invalidateAll();
    }

    function handleKeyDown(event) {
        if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault(); // Prevents a new line
            createMessage(messageContent);
            messageContent = ''; // Clear the textarea after sending the message
        }
    }

</script>


<div class="col-span-3 flex flex-col h-full">
    <Card class="max-w-full flex-grow h-full shadow-0">
        <div class="flex justify-between items-center mb-4 ">
            <h5 class="text-2xl font-bold tracking-tight text-gray-900 dark:text-white"> {conversation.name }</h5>
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
        </div>
        <form class="mt-4" on:submit|preventDefault={() => createMessage(messageContent)}>
            <label for="chat" class="sr-only">Your message</label>
            <div class="flex items-center px-3 py-2 rounded-lg dark:bg-gray-700">
        <textarea id="message" rows="1"
                  class="block mx-4 p-2.5 w-full md text-gray-900 bg-white rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-800 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                  placeholder="Your message..."
                  bind:value={messageContent}
                  on:keydown={handleKeyDown}></textarea>
                <button type="submit"
                        class="inline-flex justify-center p-2 text-blue-600 rounded-full cursor-pointer hover:bg-blue-100 dark:text-blue-500 dark:hover:bg-gray-600">
                    <svg class="w-5 h-5 rotate-90 rtl:-rotate-90" aria-hidden="true"
                         xmlns="http://www.w3.org/2000/svg"
                         fill="currentColor" viewBox="0 0 18 20">
                        <path d="m17.914 18.594-8-18a1 1 0 0 0-1.828 0l-8 18a1 1 0 0 0 1.157 1.376L8 18.281V9a1 1 0 0 1 2 0v9.281l6.758 1.689a1 1 0 0 0 1.156-1.376Z"/>
                    </svg>
                    <span class="sr-only">Send message</span>
                </button>
            </div>
        </form>
    </Card>
</div>
