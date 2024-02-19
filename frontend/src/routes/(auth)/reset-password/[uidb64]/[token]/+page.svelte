<script lang="ts">import { Register, Section } from 'flowbite-svelte-blocks';
import { Button, Helper, Input, Label } from 'flowbite-svelte';
import { resetPassword } from '../../../authService';
import { writable } from 'svelte/store';
import { goto } from '$app/navigation';

export let data;
let password1 = '';
let password2 = '';
const password1Error = writable([]);
const password2Error = writable([]);
const message = writable('');

async function handleSubmit(event: Event) {
	try {
		await resetPassword(data.uidb64, data.token, password1, password2);
		goto('/login');
	} catch (error) {
		password1Error.set(error.password1 || []);
		password2Error.set(error.password2 || []);
		message.set(error.message || []);
	}
}

</script>

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
				<h3 class="text-xl font-medium text-gray-900 dark:text-white p-0">Reset Password</h3>
				<Label class="space-y-2">
					<span>New password</span>
					<Input bind:value={password1} autocomplete="new-password" type="password" name="password" placeholder="•••••" required />
				{#if $password1Error.length}
					{#each $password1Error as error}
						<Helper color="red">{error}</Helper>
					{/each}
				{/if}
				</Label>
				<Label class="space-y-2">
					<span>Confirm new password</span>
					<Input bind:value={password2} autocomplete="new-password" type="password" name="confirm-password" placeholder="•••••" required />
				{#if $password2Error.length}
					{#each $password2Error as error}
						<Helper color="red">{error}</Helper>
					{/each}
				{/if}
				</Label>
				{#if $message}
					<Helper color="red">{$message}</Helper>
				{/if}
				<Button type="submit" class="w-full1">Reset password</Button>
			</form>
		</div>
	</Register>
</Section>