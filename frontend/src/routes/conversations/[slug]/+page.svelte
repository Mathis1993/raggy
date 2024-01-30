<script lang="ts">
    import {ActivityItem, Avatar, Breadcrumb, BreadcrumbItem, Card, TimelineItem} from "flowbite-svelte";
    import {CalendarWeekSolid} from "flowbite-svelte-icons";

    export let data;
    let conversation: Conversation = data.conversation;
    let messages: Message[] = data.conversation.messages;
</script>

<Breadcrumb class="mb-2" aria-label="Default breadcrumb example">
    <BreadcrumbItem href="/" home>Home</BreadcrumbItem>
    <BreadcrumbItem href="/conversations">conversations</BreadcrumbItem>
</Breadcrumb>

<Card class="max-w-full">
    <h5 class="mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white"> Your Conversation</h5>

    <Card class="max-w-full">

        {#each messages as message}
            <div class="flex items-start gap-2.5 my-2">
                <Avatar></Avatar>
                <div class="flex flex-col w-full max-w-[320px] leading-1.5 p-4 border-gray-200 bg-gray-100 rounded-e-xl rounded-es-xl dark:bg-gray-700">
                    <div class="flex items-center space-x-2 rtl:space-x-reverse">
                        <span class="text-sm font-semibold text-gray-900 dark:text-white">
                            {#if message.is_user_message}
                                User
                            {:else}
                                Bot
                            {/if}
                        </span>
                        <span class="text-sm font-normal text-gray-500 dark:text-gray-400">{message.created_at}</span>
                    </div>
                    <p class="text-sm font-normal py-2.5 text-gray-900 dark:text-white"> {message.text} </p>
                </div>
            </div>
        {/each}

        <form class="mt-4">
            <label for="chat" class="sr-only">Your message</label>
            <div class="flex items-center px-3 py-2 rounded-lg bg-gray-50 dark:bg-gray-700">
                <textarea id="chat" rows="1" class="block mx-4 p-2.5 w-full text-sm text-gray-900 bg-white rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-800 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="Your message..."></textarea>
                <button type="submit" class="inline-flex justify-center p-2 text-blue-600 rounded-full cursor-pointer hover:bg-blue-100 dark:text-blue-500 dark:hover:bg-gray-600">
                    <svg class="w-5 h-5 rotate-90 rtl:-rotate-90" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 18 20">
                        <path d="m17.914 18.594-8-18a1 1 0 0 0-1.828 0l-8 18a1 1 0 0 0 1.157 1.376L8 18.281V9a1 1 0 0 1 2 0v9.281l6.758 1.689a1 1 0 0 0 1.156-1.376Z"/>
                    </svg>
                    <span class="sr-only">Send message</span>
                </button>
            </div>
        </form>

    </Card>
</Card>

