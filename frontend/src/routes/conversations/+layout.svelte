<script lang="ts">
    import {Card} from "flowbite-svelte";

    export let data;
    let conversations: [Conversation] = data.conversations;
</script>

<Card class="grid grid-cols-4 max-w-full h-[calc(100vh-7vh)] p-0 sm:p-0">
    <div class="p-4 col-span-1 bg-gray-700 rounded text-white">
        <a href="/conversations/">
            <h2 class="flex text-2xl font-bold tracking-tight text-gray-50 pb-2 m-2">
                Conversations
            </h2>
        </a>
        <ul>
            {#each conversations as conversation}
                <Card class="flex max-w-full items-center bg-gray-700 text-white hover:bg-gray-500 border-gray-500 hover:border-gray-50000 shadow-gray-700">
                    <a href={`/conversations/${conversation.id}`}
                       class="flex items-center text-gray-700 dark:text-gray-200">
                        <span class="text-white">{conversation.name}</span>
                    </a>
                </Card>
            {/each}
        </ul>
    </div>
    <slot/>
</Card>
