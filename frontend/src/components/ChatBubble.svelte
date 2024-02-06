<script lang="ts">
    import {Avatar, Button, Tooltip} from "flowbite-svelte";
    import {FileCopyOutline} from "flowbite-svelte-icons";

    export let message: Message;
    let role = message.is_user_message ? 'user' : 'bot';
    let color = message.is_user_message ? 'bg-blue-100' : 'bg-gray-100';

    async function copyToClipboard() {
        try {
            await navigator.clipboard.writeText(message.text);
            console.log('Message copied to clipboard');
        } catch (err) {
            console.error('Failed to copy message: ', err);
        }
    }

</script>

<div class="flex items-start gap-2.5 my-2">
    {#if role === 'user'}
        <Avatar></Avatar>
    {:else}
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
             stroke="currentColor" class="w-10 h-10">
            <path stroke-linecap="round" stroke-linejoin="round"
                  d="M15.59 14.37a6 6 0 0 1-5.84 7.38v-4.8m5.84-2.58a14.98 14.98 0 0 0 6.16-12.12A14.98 14.98 0 0 0 9.631 8.41m5.96 5.96a14.926 14.926 0 0 1-5.841 2.58m-.119-8.54a6 6 0 0 0-7.381 5.84h4.8m2.581-5.84a14.927 14.927 0 0 0-2.58 5.84m2.699 2.7c-.103.021-.207.041-.311.06a15.09 15.09 0 0 1-2.448-2.448 14.9 14.9 0 0 1 .06-.312m-2.24 2.39a4.493 4.493 0 0 0-1.757 4.306 4.493 4.493 0 0 0 4.306-1.758M16.5 9a1.5 1.5 0 1 1-3 0 1.5 1.5 0 0 1 3 0Z"/>
        </svg>
    {/if}
    <div class={`flex flex-col w-full leading-1.5 p-4 border-gray-200 rounded-e-xl rounded-es-xl dark:bg-gray-700 ${color}`}>
        <div class="flex items-center justify-between space-x-2 rtl:space-x-reverse">
            <div class="flex items-center">
                <span class="text-sm font-semibold text-gray-900 dark:text-white">
                   {role === 'user' ? 'User' : 'Assistant'}
                </span>
                <span class="text-sm font-normal text-gray-500 dark:text-gray-400">{message.created_at}</span>
            </div>
            {#if role !== 'user'}
                <Button outline={true} on:click={copyToClipboard} class="!p-2 text-gray-500 border-gray-500" size="md">
                    <FileCopyOutline class="w-4 h-4"/>
                </Button>
                <Tooltip>Copy</Tooltip>
            {/if}
        </div>
        <p class="text-sm font-normal py-2.5 text-gray-900 dark:text-white"> {message.text} </p>
    </div>
</div>
