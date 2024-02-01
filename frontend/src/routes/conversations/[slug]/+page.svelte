<script lang="ts">
    import {Avatar, Breadcrumb, BreadcrumbItem, Card} from "flowbite-svelte";
    import ChatBubble from "../../../components/ChatBubble.svelte";
    import {onMount} from "svelte";

    export let data;
    let conversation: Conversation = data.conversation;
    let messages: Message[] = data.conversation.messages;

    // auto scroll to bottom
    let chatContainer: ChatBubble;
    onMount(() => {
        chatContainer.scrollTop = chatContainer.scrollHeight;
    });

    async function handleSubmit(event) {
        event.preventDefault();
        const message = event.target.elements.message.value;
        const response = await fetch('http://localhost:8000/api/conversations/' + conversation.id + "/messages/", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({"message": message}),
        });

        if (!response.ok) {
            console.error('Failed to send message', response);
            return;
        }

        event.target.elements.chat.value = '';
        location.reload();
    }
</script>


<div class="col-span-3 flex flex-col h-full">
    <Card class="max-w-full flex-grow h-full shadow-0">
        <h5 class="mb-4 text-2xl font-bold tracking-tight text-gray-900 dark:text-white"> {conversation.name }</h5>
        <div class="max-w-full h-[calc(100vh-35vh)] flex-grow overflow-auto" bind:this={chatContainer}>
            {#each messages as message}
                <ChatBubble {message}/>
            {/each}
        </div>
        <form class="mt-4" on:submit|preventDefault={handleSubmit}>
            <label for="chat" class="sr-only">Your message</label>
            <div class="flex items-center px-3 py-2 rounded-lg dark:bg-gray-700">
        <textarea id="message" rows="1"
                  class="block mx-4 p-2.5 w-full md text-gray-900 bg-white rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-800 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                  placeholder="Your message..."></textarea>
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
