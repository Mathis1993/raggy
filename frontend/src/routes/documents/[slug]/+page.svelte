<script lang="ts">
    import {ActivityItem, Breadcrumb, BreadcrumbItem, Card, TimelineItem} from "flowbite-svelte";
    import {CalendarWeekSolid} from "flowbite-svelte-icons";

    export let data;
    let document: ContextDocument = data.document;
</script>

<Breadcrumb class="mb-2" aria-label="Default breadcrumb example">
    <BreadcrumbItem href="/" home>Home</BreadcrumbItem>
    <BreadcrumbItem href="/conversations">Documents</BreadcrumbItem>
    <BreadcrumbItem href="/conversations">Document ({document.id})</BreadcrumbItem>
</Breadcrumb>

<Card class="max-w-full">
    <h5 class="mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white"> {document.name} </h5>

    <TimelineItem title={document.name} date={document.created_at}>
        <svelte:fragment slot="icon">
                    <span class="flex absolute -start-3 justify-center items-center w-6 h-6 bg-primary-200 rounded-full ring-8 ring-white dark:ring-gray-900 dark:bg-primary-900">
                        <CalendarWeekSolid class="w-3 h-3 text-primary-600 dark:text-primary-400"/>
                    </span>
        </svelte:fragment>
        <p class="text-base font-normal text-gray-500 dark:text-gray-400">{document.url}</p>
    </TimelineItem>
</Card>

