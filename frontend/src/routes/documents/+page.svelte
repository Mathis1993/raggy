<script lang="ts">
    import {
        Breadcrumb,
        BreadcrumbItem,
        Button,
        Card, Input, Label, Modal, Spinner,
        Table,
        TableBody,
        TableBodyCell,
        TableBodyRow,
        TableHead,
        TableHeadCell
    } from "flowbite-svelte";
    import {Document} from "postcss";
    import {goto, invalidate} from "$app/navigation";
    import {createDocument, deleteDocument, getDocuments} from "./documentService";
    import {ExclamationCircleOutline} from "flowbite-svelte-icons";

    export let data;
    let documents: [ContextDocument] = data.documents;

    let createModalVisible: boolean = false;
    let deleteModalVisible: boolean = false;

    let document_url: string = '';
    let createProcessIsRunning: boolean = false;

    async function handleCreate(document_url: string) {
        createProcessIsRunning = true;
        await createDocument(document_url);
        createModalVisible = false;
        createProcessIsRunning = false;
        // TODO: fix invalidation and reloading of the data
        await invalidate('/documents');
    }

    let documentToDelete: any = null;
    async function handleDelete() {
        if (documentToDelete !== null) {
            await deleteDocument(documentToDelete);
            deleteModalVisible = false;
            // TODO: fix invalidation and reloading of the data
            await invalidate('/documents');
        }
    }

</script>

<Card class="max-w-full w-full">
    <h5 class="mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white"> Uploaded Documents</h5>
    <p class="font-normal text-gray-700 dark:text-gray-400 leading-tight"> This is a list of your uploaded documents </p>

    <div class="flex justify-end my-2">
        <Button on:click={() => (createModalVisible = true)}>Add Document</Button>
    </div>

    <Table hoverable={true}>
        <TableHead>
            <TableHeadCell>Document Name</TableHeadCell>
            <TableHeadCell>URL</TableHeadCell>
            <TableHeadCell>
                <span class="sr-only">Details</span>
            </TableHeadCell>
        </TableHead>
        <TableBody class="divide-y">
            {#each documents as document}
                <TableBodyRow>
                    <TableBodyCell>{document.title ? document.title.substring(0, 50) : 'No title'}</TableBodyCell>
                    <TableBodyCell>{document.identifier}</TableBodyCell>
                    <TableBodyCell>
                        <a href="/documents/{document.id}/" class="font-medium text-primary-600 hover:underline dark:text-primary-500">View</a>
                    </TableBodyCell>
                    <TableBodyCell>
                        <Button on:click={() => {deleteModalVisible = true; documentToDelete = document.id;}}>Delete</Button>
                    </TableBodyCell>
                </TableBodyRow>
            {/each}
        </TableBody>
    </Table>
</Card>


<Modal bind:open={createModalVisible} size="xs" autoclose={false} outsideclose={true} class="w-full">
    <form class="flex flex-col space-y-6" on:submit|preventDefault={() => handleCreate(document_url)}>
        <h3 class="mb-4 text-xl font-medium text-gray-900 dark:text-white">Add a new document</h3>
        <Label class="space-y-2">
            <span>URL</span>
            <Input bind:value={document_url} type="url" name="url" placeholder="www.company.com" required />
        </Label>
        <Button type="submit" class="w-full1" disabled={createProcessIsRunning}>
            {#if createProcessIsRunning}
                <Spinner/>
            {:else}
                Add
            {/if}
        </Button>
    </form>
</Modal>


<Modal bind:open={deleteModalVisible} autoclose={false} outsideclose={true} size="xs">
    <div class="text-center">
        <ExclamationCircleOutline class="mx-auto mb-4 text-gray-400 w-12 h-12 dark:text-gray-200" />
        <h3 class="mb-5 text-lg font-normal text-gray-500 dark:text-gray-400">Are you sure you want to remove this document?</h3>
        <Button on:click={handleDelete} color="red" class="me-2">Yes, I'm sure</Button>
        <Button color="alternative">No, cancel</Button>
    </div>
</Modal>