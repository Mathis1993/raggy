<script lang="ts">
    import { Button, Textarea } from 'flowbite-svelte';
    import { PapperPlaneOutline } from 'flowbite-svelte-icons';
    import { createConversation } from "./conversationService";
    import { user } from '../../../stores/userStore';
    import ConversationHistory from '../../../components/ConversationHistory.svelte';
    
    let messageContent = '';
    let rows = 3; // Default to 3 rows
    
    $: rows = Math.max(3, messageContent.split('\n').length);
    
    async function handleSubmit() {
        if (!messageContent.trim()) return;
        const conversation = await createConversation();
        messageContent = '';
    }

    function handleKeyDown(event: KeyboardEvent) {
        if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault();
            handleSubmit();
        }
    }
</script>

<div class="flex h-[calc(100vh-4rem)] relative bg-gray-50 dark:bg-gray-900 overflow-hidden">
    <div class="flex-1 flex items-center justify-center content-wrapper">
        <div class="w-full max-w-3xl px-4">
            <div class="text-center mb-12">
                <h1 class="text-4xl font-bold text-gray-900 dark:text-white mb-4">
                    Hello, {$user.first_name || 'there'}
                </h1>
                <p class="text-lg text-gray-600 dark:text-gray-400">
                    Start a new conversation by typing your message below
                </p>
            </div>

            <div class="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
                <form on:submit|preventDefault={handleSubmit}>
                    <div class="flex flex-col gap-4">
                        <Textarea
                            id="message"
                            class="w-full resize-none rounded-lg border border-gray-200 dark:border-gray-600 bg-white dark:bg-gray-700 px-4 py-3 text-lg"
                            {rows}
                            placeholder="Type your message to start a new conversation..."
                            bind:value={messageContent}
                            on:keydown={handleKeyDown}
                        />
                        <div class="flex justify-end">
                            <Button type="submit" color="blue" class="px-6">
                                <div class="flex items-center gap-2">
                                    <span>Start Conversation</span>
                                    <PapperPlaneOutline class="w-4 h-4 rotate-45"/>
                                </div>
                            </Button>
                        </div>
                    </div>
                </form>
            </div>
        </div>
    </div>

    <ConversationHistory currentConversationId={null} />
</div>


