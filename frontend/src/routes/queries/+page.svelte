<script lang="ts">
	import { Button, Heading, Search, Spinner } from 'flowbite-svelte';

	const QUESTION_API_ENDPOINT: string = 'http://localhost:8000/api/questions/create';

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
			body: JSON.stringify({ 'question': question })
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

<div class="m-4">
	<Heading tag="h3">Overview</Heading>

	<div class="mt-4">
		<form on:submit={handleSubmit}>
			<Search bind:value={question} name="question" />
			<Button type="submit">Submit</Button>
		</form>
	</div>

	<div class="mt-4">
		{#if submitted}
			<Spinner />
		{/if}

		{#if answer}
			<div class="response">
				<p>{answer}</p>
			</div>
		{/if}
	</div>

</div>
