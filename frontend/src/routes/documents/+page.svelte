<script lang="ts">
    import {
        Breadcrumb,
        BreadcrumbItem,
        Button,
        Card,
        Table,
        TableBody,
        TableBodyCell,
        TableBodyRow,
        TableHead,
        TableHeadCell
    } from "flowbite-svelte";
    import {Document} from "postcss";

    export let data;
    let documents: [ContextDocument] = data.documents;

    async function deleteDocument(documentId: number) {
        const response = await fetch('http://localhost:8000/api/documents/' + documentId + '/', {
            method: 'DELETE',
        });
        if (!response.ok) {
            console.error('Failed to delete document', response.status);
        }
        location.reload();
    }
</script>

<Card class="max-w-full w-full">
    <h5 class="mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white"> Uploaded Documents</h5>
    <p class="font-normal text-gray-700 dark:text-gray-400 leading-tight"> This is a list of your uploaded documents </p>

    <div class="flex justify-end my-2">
        <Button href="/documents/create">Add Document</Button>
    </div>

    <Table hoverable={true}>
        <TableHead>
            <TableHeadCell>Document Name</TableHeadCell>
            <TableHeadCell>URL</TableHeadCell>
            <TableHeadCell>Created At</TableHeadCell>
            <TableHeadCell>
                <span class="sr-only">Details</span>
            </TableHeadCell>
        </TableHead>
        <TableBody class="divide-y">
            {#each documents as document}
                <TableBodyRow>
                    <TableBodyCell>{document.title}</TableBodyCell>
                    <TableBodyCell>{document.identifier}</TableBodyCell>
                    <TableBodyCell>{document.created_at}</TableBodyCell>
                    <TableBodyCell>
                        <a href="/documents/{document.id}/" class="font-medium text-primary-600 hover:underline dark:text-primary-500">View</a>
                    </TableBodyCell>
                    <TableBodyCell>
                        <Button on:click={() => deleteDocument(document.id)} variant="danger">Delete</Button>                    </TableBodyCell>
                </TableBodyRow>
            {/each}
        </TableBody>
    </Table>
</Card>