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
    import {goto} from "$app/navigation";

    async function createConversation() {
        console.log('Creating conversation');
        const response = await fetch('http://localhost:8080/api/conversations/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
        });

        if (!response.ok) {
            console.error('Failed to create conversation');
            return;
        }

        console.log('Conversation created');

        const data = await response.json();
        goto(`/conversations/${data.id}`);
    };
</script>

<div class="col-span-3 flex items-center justify-center">
    <form class="mt-4" on:submit|preventDefault={createConversation}>
        <Button> Create </Button>
    </form>
</div>


