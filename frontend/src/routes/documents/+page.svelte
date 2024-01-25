<script lang="ts">
    import {
        Breadcrumb,
        BreadcrumbItem,
        Button,
        Card,
        Table, TableBody, TableBodyCell, TableBodyRow,
        TableHead,
        TableHeadCell,
        Timeline,
        TimelineItem
    } from "flowbite-svelte";
    import {CalendarWeekSolid} from "flowbite-svelte-icons";
</script>

<Breadcrumb class="mb-2" aria-label="Default breadcrumb example">
    <BreadcrumbItem href="/" home>Home</BreadcrumbItem>
    <BreadcrumbItem href="/questions">Documents</BreadcrumbItem>
</Breadcrumb>

<Card class="max-w-full">
    <h5 class="mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white"> Your Uploaded Documents</h5>
    <p class="font-normal text-gray-700 dark:text-gray-400 leading-tight"> This is a list of your uploaded documents </p>

    <div class="flex justify-end my-2">
        <Button href="/documents/create">Add Document</Button>
    </div>

    <Table hoverable={true}>
        <TableHead>
            <TableHeadCell>Product name</TableHeadCell>
            <TableHeadCell>Color</TableHeadCell>
            <TableHeadCell>Category</TableHeadCell>
            <TableHeadCell>Price</TableHeadCell>
            <TableHeadCell>
                <span class="sr-only">Edit</span>
            </TableHeadCell>
        </TableHead>
        <TableBody class="divide-y">
            <TableBodyRow>
                <TableBodyCell>Apple MacBook Pro 17"</TableBodyCell>
                <TableBodyCell>Sliver</TableBodyCell>
                <TableBodyCell>Laptop</TableBodyCell>
                <TableBodyCell>$2999</TableBodyCell>
                <TableBodyCell>
                    <a href="/tables" class="font-medium text-primary-600 hover:underline dark:text-primary-500">Edit</a>
                </TableBodyCell>
            </TableBodyRow>
            <TableBodyRow>
                <TableBodyCell>Microsoft Surface Pro</TableBodyCell>
                <TableBodyCell>White</TableBodyCell>
                <TableBodyCell>Laptop PC</TableBodyCell>
                <TableBodyCell>$1999</TableBodyCell>
                <TableBodyCell>
                    <a href="/tables" class="font-medium text-primary-600 hover:underline dark:text-primary-500">Edit</a>
                </TableBodyCell>
            </TableBodyRow>
            <TableBodyRow>
                <TableBodyCell>Magic Mouse 2</TableBodyCell>
                <TableBodyCell>Black</TableBodyCell>
                <TableBodyCell>Accessories</TableBodyCell>
                <TableBodyCell>$99</TableBodyCell>
                <TableBodyCell>
                    <a href="/tables" class="font-medium text-primary-600 hover:underline dark:text-primary-500">Edit</a>
                </TableBodyCell>
            </TableBodyRow>
        </TableBody>
    </Table>

</Card>