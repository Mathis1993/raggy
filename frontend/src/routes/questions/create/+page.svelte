<script lang="ts">
    import {Button, Card, Search, Spinner} from 'flowbite-svelte';

    const QUESTION_API_ENDPOINT: string = 'http://localhost:8000/api/questions/';

    let question: string = '';
    let answer: string = null;
    let submitted: boolean = false;

    async function handleSubmit(request: Event) {
        request.preventDefault();
        submitted = true;
        const response = await fetch(QUESTION_API_ENDPOINT, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({'question': question})
        });

        if (response.ok) {
            let apiResponse = await response.json();
            console.log(apiResponse);
            answer = apiResponse['answer'];
            // Handle the response data
        } else {
            console.error('Error in API response');
        }
        submitted = false;
    }

</script>

<Card class="max-w-full">
    <h5 class="mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white">Ask a new question</h5>
    <div class="mt-4">
        <form on:submit={handleSubmit}>
            <Search bind:value={question} name="question">
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
