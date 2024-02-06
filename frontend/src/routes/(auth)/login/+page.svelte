<script lang="ts">
	import { Register, Section } from 'flowbite-svelte-blocks';
	import { Button, Input, Label, NavBrand } from 'flowbite-svelte';

</script>

<Section name="login">
	<Register href="/">
		<svelte:fragment slot="top">
			<NavBrand href="/">
				<span class="self-center whitespace-nowrap text-xl font-semibold dark:text-white">Raggy</span>
				<svg class="w-6 h-6 text-gray-800 dark:text-white" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
					<path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16.9 9.7 20 6.6 17.4 4 4 17.4 6.6 20 16.9 9.7Zm0 0L14.3 7M6 7v2m0 0v2m0-2H4m2 0h2m7 7v2m0 0v2m0-2h-2m2 0h2M8 4h0v0h0v0Zm2 2h0v0h0v0Zm2-2h0v0h0v0Zm8 8h0v0h0v0Zm-2 2h0v0h0v0Zm2 2h0v0h0v0Z"/>
				</svg>
			</NavBrand>
		</svelte:fragment>
		<div class="p-6 space-y-4 md:space-y-6 sm:p-8">
			<form class="flex flex-col space-y-6" method="POST" action="?/post">
				<h3 class="text-xl font-medium text-gray-900 dark:text-white p-0">Sign In</h3>
				<Label class="space-y-2">
					<span>Your email</span>
					<Input type="email" name="email" placeholder="name@company.com" required />
				</Label>
				<Label class="space-y-2">
					<span>Your password</span>
					<Input type="password" name="password" placeholder="•••••" required />
				</Label>
				<div class="flex items-start">
					<a href="/static" class="ml-auto text-sm text-blue-700 hover:underline dark:text-blue-500">Forgot password?</a>
				</div>
				<Button type="submit" class="w-full1">Sign in</Button>
				<p class="text-sm font-light text-gray-500 dark:text-gray-400">
					Don’t have an account yet? <a href="/static" class="font-medium text-primary-600 hover:underline dark:text-primary-500">Sign up</a>
				</p>
			</form>
		</div>
	</Register>
</Section>