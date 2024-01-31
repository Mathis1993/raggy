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
</script>

<Breadcrumb class="mb-2" aria-label="Default breadcrumb example">
    <BreadcrumbItem href="/" home>Home</BreadcrumbItem>
    <BreadcrumbItem href="/conversations">Conversations</BreadcrumbItem>
</Breadcrumb>


<h2 class="py-4 text-2xl font-semibold text-gray-800 dark:text-gray-200">Conversations</h2>

<Card class="grid grid-cols-4 max-w-full p-0 sm:p-0">
    <div class="col-span-1 p-2 bg-gray-700 rounded text-white">
        <ul>
            <Card class="flex items-center bg-gray-700 text-white hover:bg-gray-500 border-gray-500 hover:border-gray-50000 shadow-gray-700">
                <a href={`/conversations/${conversation.id}`}
                   class="flex items-center text-gray-700 dark:text-gray-200">
                    <span class="text-white">{conversation.name}</span>
                </a>
            </Card>
        </ul>
    </div>
    <div class="col-span-3">
        <Card class="max-w-full">
            <h5 class="mb-4 text-2xl font-bold tracking-tight text-gray-900 dark:text-white"> {conversation.name }</h5>

            <div class="max-w-full overflow-y-auto max-h-[600px]" bind:this={chatContainer}>
                {#each messages as message}
                    <ChatBubble {message}/>
                {/each}

                <form class="mt-4">
                    <label for="chat" class="sr-only">Your message</label>
                    <div class="flex items-center px-3 py-2 rounded-lg dark:bg-gray-700">
                <textarea id="chat" rows="1"
                          class="block mx-4 p-2.5 w-full text-sm text-gray-900 bg-white rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-800 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
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

            </div>
        </Card>
    </div>
</Card>