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

<div class="col-span-3 flex items-center justify-center">
    <div class=" my-2">
        <Button href="/conversations/create">Start Conversation</Button>
    </div>
</div>


