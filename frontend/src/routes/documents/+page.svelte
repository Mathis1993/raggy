<script lang="ts">
    import {
        Button,
        Card,
        Input,
        Label,
        Modal,
        Spinner,
        Table,
        TableBody,
        TableBodyCell,
        TableBodyRow,
        TableHead,
        TableHeadCell
    } from "flowbite-svelte";
    import {invalidate} from "$app/navigation";
    import {createDocument, deleteDocument, retrieveDocument} from "./documentService";
    import {ExclamationCircleOutline, TrashBinOutline, EyeOutline} from "flowbite-svelte-icons";

    export let data;
    let documents: [ContextDocument] = data.documents;

    let createModalVisible: boolean = false;
    let deleteModalVisible: boolean = false;
    let detailModalVisible: boolean = false;

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

    let documentDetails: any = null;
    async function handleView(documentId: number) {
        if (documentId != null) {
            documentDetails = await retrieveDocument(documentId);
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
            <TableHeadCell></TableHeadCell>
        </TableHead>
        <TableBody>
            {#each documents as document}
                <TableBodyRow>
                    <TableBodyCell>{document.title ? document.title.substring(0, 50) : 'No title'}</TableBodyCell>
                    <TableBodyCell>{document.identifier}</TableBodyCell>
                    <TableBodyCell class="flex items-center justify-between">
                        <Button outline={true} on:click={async () => {detailModalVisible = true; await handleView(document.id);}} class="border-primary-400 hover:bg-primary-200">
                            <EyeOutline class="text-primary-600"/>
                        </Button>
                    </TableBodyCell>
                </TableBodyRow>
            {/each}
        </TableBody>
    </Table>
</Card>


<Modal bind:open={createModalVisible} size="xs" autoclose={false} outsideclose class="w-full">
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


<Modal bind:open={deleteModalVisible} autoclose={false} outsideclose size="xs">
    <div class="text-center">
        <ExclamationCircleOutline class="mx-auto mb-4 text-gray-400 w-12 h-12 dark:text-gray-200" />
        <h3 class="mb-5 text-lg font-normal text-gray-500 dark:text-gray-400">Are you sure you want to remove this document?</h3>
        <Button on:click={handleDelete} color="red" class="me-2">Yes, I'm sure</Button>
        <Button color="alternative" on:click={() => {deleteModalVisible=false}}>No, cancel</Button>
    </div>
</Modal>

<Modal bind:open={deleteModalVisible} autoclose={false} outsideclose size="xs">
    <div class="text-center">
        <ExclamationCircleOutline class="mx-auto mb-4 text-gray-400 w-12 h-12 dark:text-gray-200" />
        <h3 class="mb-5 text-lg font-normal text-gray-500 dark:text-gray-400">Are you sure you want to remove this document?</h3>
        <Button on:click={handleDelete} color="red" class="me-2">Yes, I'm sure</Button>
        <Button color="alternative" on:click={() => {deleteModalVisible=false}}>No, cancel</Button>
    </div>
</Modal>

<Modal title="" bind:open={detailModalVisible} autoclose outsideclose size="sm">
    <div class="flex justify-between mb-4 rounded-t sm:mb-5">
        <div class="text-lg text-gray-900 md:text-xl dark:text-white">
            <h3 class="font-semibold">{documentDetails ? documentDetails.title : 'Loading...'}</h3>
        </div>
    </div>
    <dl>
        <dt class="mb-2 font-semibold leading-none text-gray-900 dark:text-white">Identifier</dt>
        <dd class="mb-4 font-light text-gray-500 sm:mb-5 dark:text-gray-400">{documentDetails ? documentDetails.identifier : 'Loading...'}</dd>
        <dt class="mb-2 font-semibold leading-none text-gray-900 dark:text-white">Created At</dt>
        <dd class="mb-4 font-light text-gray-500 sm:mb-5 dark:text-gray-400">{documentDetails ? documentDetails.created_at : 'Loading...'}</dd>
    </dl>
    <div class="flex justify-between items-center">
        <div class="flex items-center space-x-3 sm:space-x-4">
<!--            <Button>-->
<!--                <svg aria-hidden="true" class="mr-1 -ml-1 w-5 h-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path d="M17.414 2.586a2 2 0 00-2.828 0L7 10.172V13h2.828l7.586-7.586a2 2 0 000-2.828z" /><path fill-rule="evenodd" d="M2 6a2 2 0 012-2h4a1 1 0 010 2H4v10h10v-4a1 1 0 112 0v4a2 2 0 01-2 2H4a2 2 0 01-2-2V6z" clip-rule="evenodd" /></svg>-->
<!--                Edit-->
<!--            </Button>-->
        </div>
        <Button color="red" on:click={() => {deleteModalVisible = true; documentToDelete = documentDetails.id;}}>
            <svg aria-hidden="true" class="w-5 h-5 mr-1.5 -ml-1" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clip-rule="evenodd" /></svg>
            Delete
        </Button>
    </div>
</Modal>