<script lang="ts">
    import {
        Activity,
        ActivityItem,
        Breadcrumb,
        BreadcrumbItem,
        Button,
        Card,
        Timeline,
        TimelineItem
    } from 'flowbite-svelte';
    import {CalendarWeekSolid} from "flowbite-svelte-icons";

    /** @type {import('./$types').PageData} */
    export let data;
    let conversations: [Conversation] = data.conversations;
</script>

<Breadcrumb class="mb-2" aria-label="Default breadcrumb example">
    <BreadcrumbItem href="/" home>Home</BreadcrumbItem>
    <BreadcrumbItem href="/conversations">Conversations</BreadcrumbItem>
</Breadcrumb>

<Card class="max-w-full">
    <h5 class="mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white"> Your Recent Conversations</h5>
    <p class="font-normal text-gray-700 dark:text-gray-400 leading-tight"> This is a list of your most recent
        activity. </p>

    <div class="flex justify-end my-2">
        <Button href="/conversations/create">Start Conversation</Button>
    </div>

    <Timeline order="vertical">
        {#each conversations as conversation}
            <a href="{`/conversations/${conversation.id}`}">
                <TimelineItem title={conversation.name} date={conversation.created_at}>
                    <svelte:fragment slot="icon">
                    <span class="flex absolute -start-3 justify-center items-center w-6 h-6 bg-primary-200 rounded-full ring-8 ring-white dark:ring-gray-900 dark:bg-primary-900">
                        <CalendarWeekSolid class="w-3 h-3 text-primary-600 dark:text-primary-400"/>
                    </span>
                    </svelte:fragment>
                    <p class="text-base font-normal text-gray-500 dark:text-gray-400">{conversation.name}</p>
                </TimelineItem>
            </a>
        {/each}
    </Timeline>
</Card>

