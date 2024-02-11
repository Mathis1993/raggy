<script lang="ts">import { Register, Section } from 'flowbite-svelte-blocks';
import { Button, Input, Label } from 'flowbite-svelte';
import { getCsrfToken } from '$lib/cookies';
import { goto } from '$app/navigation';

async function handleSubmit(event) {
	const form = event.target;
	const formData = new FormData(form);
	const body = JSON.stringify({
		'email': formData.get('email') as string,
		'password1': formData.get('password1') as string,
		'password2': formData.get('password2') as string,
		'first_name': formData.get('first_name') as string,
		'last_name': formData.get('last_name') as string,
	});

	const response = await fetch('http://127.0.0.1:8000/users/signup/', {
		method: 'POST',
		credentials: 'include',
		body: body,
		headers: {
			'Content-Type': 'application/json',
			'X-CSRFToken': getCsrfToken(),
		},
	});

	if (response.status != 201) {
		const error = await response.json();
		return { status: 'error', error };
	}
	await goto('/login');
}

</script>

<Section name="register">
	<Register href="/">
		<svelte:fragment slot="top">
			<span class="self-center whitespace-nowrap text-xl font-semibold dark:text-white">Raggy</span>
			<svg class="w-6 h-6 text-gray-800 dark:text-white" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
				<path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16.9 9.7 20 6.6 17.4 4 4 17.4 6.6 20 16.9 9.7Zm0 0L14.3 7M6 7v2m0 0v2m0-2H4m2 0h2m7 7v2m0 0v2m0-2h-2m2 0h2M8 4h0v0h0v0Zm2 2h0v0h0v0Zm2-2h0v0h0v0Zm8 8h0v0h0v0Zm-2 2h0v0h0v0Zm2 2h0v0h0v0Z"/>
			</svg>
		</svelte:fragment>
		<div class="p-6 space-y-4 md:space-y-6 sm:p-8">
			<form class="flex flex-col space-y-6" on:submit|preventDefault={handleSubmit}>
				<h3 class="text-xl font-medium text-gray-900 dark:text-white p-0">Sign Up</h3>
				<Label class="space-y-2">
					<span>Your email</span>
					<Input type="email" name="email" placeholder="name@company.com" required />
				</Label>
				<Label class="space-y-2">
					<span>Your first name</span>
					<Input type="text" name="first_name" placeholder="John" />
				</Label>
				<Label class="space-y-2">
					<span>Your last name</span>
					<Input type="text" name="last_name" placeholder="Doe" />
				</Label>
				<Label class="space-y-2">
					<span>Your password</span>
					<Input type="password" name="password1" placeholder="•••••" required />
				</Label>
				<Label class="space-y-2">
					<span>Confirm password</span>
					<Input type="password" name="password2" placeholder="•••••" required />
				</Label>
<!--				<div class="flex items-start">-->
<!--					<Checkbox>I accept the <a class="font-medium text-primary-600 hover:underline dark:text-primary-500" href="/"> Terms and Conditions</a></Checkbox>-->
<!--				</div>-->
				<Button type="submit" class="w-full1">Sign up</Button>
				<div class="text-sm font-medium text-gray-500 dark:text-gray-300">
					Already have an account? <a href="/login" class="font-medium text-primary-600 hover:underline dark:text-primary-500">Sign in here</a>
				</div>
			</form>
		</div>
	</Register>
</Section>