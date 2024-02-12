<script>
	import {Button, Card, Input, Label} from 'flowbite-svelte';
	import { getCsrfToken } from '$lib/cookies';
	import { user } from '../../../stores/userStore';

	async function handleSubmit(event) {
		const form = event.target;
		const formData = new FormData(form);
		const body = JSON.stringify(Object.fromEntries(formData));
		const response = await fetch('http://127.0.0.1:8000/users/update/', {
			method: 'PUT',
			credentials: 'include',
			headers: {
				'Content-Type': 'application/json',
				'X-CSRFToken': getCsrfToken(),
			},
			body: body
		});
		if (response.ok) {
			const newUser = await response.json();
			user.set(newUser);
			return { status: 'success', user };
		}
		const error = await response.json();
		return { status: 'error', error };
	}

</script>

<Card class="max-w-full w-full">
	<h5 class="mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white"> User Settings Documents</h5>
	<p class="mb-6 font-normal text-gray-700 dark:text-gray-400 leading-tight">
		Here you can update your personal information.
	</p>

	<form on:submit|preventDefault={handleSubmit}>
		<div class="grid gap-6 mb-6 md:grid-cols-2">
			<div class="mb-3">
				<Label for="first_name" class="mb-2">First name</Label>
				<Input type="text" name="first_name" bind:value={$user.first_name} />
			</div>
			<div>
				<Label for="last_name" class="mb-2">Last name</Label>
				<Input type="text" name="last_name" bind:value={$user.last_name} />
			</div>
		</div>
		<div class="mb-4">
			<Label for="email" class="mb-2">Email address</Label>
			<Input type="email" name="email" required bind:value={$user.email} />
		</div>
		<Button type="submit">Save </Button>
	</form>
</Card>