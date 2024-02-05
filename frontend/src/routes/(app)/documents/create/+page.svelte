<script lang="ts">
    import {Breadcrumb, BreadcrumbItem, Button, Card, Search, Spinner} from 'flowbite-svelte';

    const DOCUMENT_API_ENDPOINT: string = 'http://127.0.0.1:8000/api/documents/';

    let document_url: string = '';
    let submitted: boolean = false;

    async function handleSubmit(request: Event) {
        request.preventDefault();
        submitted = true;
        const response = await fetch(DOCUMENT_API_ENDPOINT, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({'document_url': document_url})
        });

        if (response.ok) {
            let apiResponse = await response.json();
            console.log(apiResponse);
            // Handle the response data
        } else {
            console.error('Error in API response');
        }
        submitted = false;
    }

</script>

<Breadcrumb class="mb-2" aria-label="Default breadcrumb example">
    <BreadcrumbItem href="/" home>Home</BreadcrumbItem>
    <BreadcrumbItem href="/documents">Documents</BreadcrumbItem>
</Breadcrumb>

<Card class="max-w-full">
    <h5 class="mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white">Add a new document URL</h5>
    <div class="mt-4">
        <form on:submit={handleSubmit}>
            <Search bind:value={document_url} name="document_url">
                <Button type="submit">Submit</Button>
            </Search>
        </form>
    </div>

    <div class="mt-4">
        {#if submitted}
            <Spinner/>
        {/if}
    </div>
</Card>
