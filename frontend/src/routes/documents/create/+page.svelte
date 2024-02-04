<script lang="ts">
    import {Breadcrumb, BreadcrumbItem, Button, Card, Search, Spinner} from 'flowbite-svelte';
    import {goto} from "$app/navigation";

    const DOCUMENT_API_ENDPOINT: string = 'http://localhost:8000/api/documents/';

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
        goto('/documents')
    }

</script>


<Card class="max-w-full w-full">
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
