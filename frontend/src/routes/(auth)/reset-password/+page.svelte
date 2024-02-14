<script lang="ts">import { Register, Section } from 'flowbite-svelte-blocks';
import { Button, Input, Label, Modal } from 'flowbite-svelte';
import { writable } from 'svelte/store';
import { resetPassword } from '../authService';

let email = '';
let resetError = writable('');
let popupVisible = writable(false);

async function handleSubmit(event) {
	try {
		await resetPassword(email);
		popupVisible.set(true);
	} catch (error) {
		resetError.set(error.message || 'An error occurred during the password reset.');
	}
}
</script>

{#if popupVisible}
	<!-- ToDo: Format the popup text (shows just in plain text right now) -->
	<Modal open={$popupVisible} autoclose={false} outsideclose size="xs">
		<div class="text-center">
			<h2>Password Reset Successful</h2>
			<p>If a user with that email exists, a password reset link has been sent.</p>
			<p>Please check your email for further instructions.</p>
			<p>Don't forget to check your spam folder.</p>
		</div>
	</Modal>
{/if}

<Section name="reset" sectionClass="w-1/2">
	<Register href="/">
		<svelte:fragment slot="top">
			<span class="self-center whitespace-nowrap text-xl font-semibold dark:text-white">Raggy</span>
			<svg class="w-6 h-6 text-gray-800 dark:text-white" aria-hidden="true" xmlns="http://www.w3.org/2000/svg"
					 fill="none" viewBox="0 0 24 24">
				<path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
							d="M16.9 9.7 20 6.6 17.4 4 4 17.4 6.6 20 16.9 9.7Zm0 0L14.3 7M6 7v2m0 0v2m0-2H4m2 0h2m7 7v2m0 0v2m0-2h-2m2 0h2M8 4h0v0h0v0Zm2 2h0v0h0v0Zm2-2h0v0h0v0Zm8 8h0v0h0v0Zm-2 2h0v0h0v0Zm2 2h0v0h0v0Z"/>
			</svg>
		</svelte:fragment>
		<div class="p-6 space-y-4 md:space-y-6 sm:p-8">
			<form class="flex flex-col space-y-6" on:submit|preventDefault={handleSubmit}>
				<h3 class="text-xl font-medium text-gray-900 dark:text-white p-0">Forgot your Password?</h3>
				<Label class="space-y-2">
					<span>Your email</span>
					<Input bind:value={email} autocomplete="email" type="email" name="email" placeholder="name@company.com" required />
				</Label>
				{#if $resetError}
					<p class="text-red-500">{ $resetError }</p>
				{/if}
				<Button type="submit" class="w-full1">Reset passwod</Button>
			</form>
		</div>
	</Register>
</Section>