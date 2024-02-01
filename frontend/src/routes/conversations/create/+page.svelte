<script lang="ts">
    import {Breadcrumb, BreadcrumbItem, Button, Card, Search, Spinner} from 'flowbite-svelte';

    const CONVERSATION_API_ENDPOINT: string = 'http://localhost:8000/api/questions/';

    let conversation: string = '';
    let answer: string = null;
    let submitted: boolean = false;

    async function handleSubmit(request: Event) {
        request.preventDefault();
        submitted = true;
        const response = await fetch(CONVERSATION_API_ENDPOINT, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({'conversation': conversation})
        });

        if (response.ok) {
            let apiResponse = await response.json();
            console.log(apiResponse);
            answer = apiResponse["conversation"].answer;
        } else {
            console.error('Error in API response');
        }
        submitted = false;
    }

</script>

<Breadcrumb class="mb-2" aria-label="Default breadcrumb example">
    <BreadcrumbItem href="/" home>Home</BreadcrumbItem>
    <BreadcrumbItem href="/conversations">conversations</BreadcrumbItem>
</Breadcrumb>

<Card class="max-w-full">
    <h5 class="mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white">Ask a new conversation</h5>
    <div class="mt-4">
        <form on:submit={handleSubmit}>
            <Search bind:value={conversation} name="conversation">
                <Button type="submit">Submit</Button>
            </Search>
        </form>
    </div>

    <div class="mt-4">
        {#if submitted}
            <Spinner/>
        {/if}

        {#if answer}
            <div class="response">
                <p>{answer}</p>
            </div>
        {/if}
    </div>
</Card>
