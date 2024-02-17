<script lang="ts">import { Register, Section } from 'flowbite-svelte-blocks';
import { Button } from 'flowbite-svelte';

export let data;

</script>

<Section name="reset" sectionClass="w-1/2">
	<Register href="/login">
		<svelte:fragment slot="top">
			<span class="self-center whitespace-nowrap text-xl font-semibold dark:text-white">Raggy</span>
			<svg class="w-6 h-6 text-gray-800 dark:text-white" aria-hidden="true" xmlns="http://www.w3.org/2000/svg"
					 fill="none" viewBox="0 0 24 24">
				<path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
							d="M16.9 9.7 20 6.6 17.4 4 4 17.4 6.6 20 16.9 9.7Zm0 0L14.3 7M6 7v2m0 0v2m0-2H4m2 0h2m7 7v2m0 0v2m0-2h-2m2 0h2M8 4h0v0h0v0Zm2 2h0v0h0v0Zm2-2h0v0h0v0Zm8 8h0v0h0v0Zm-2 2h0v0h0v0Zm2 2h0v0h0v0Z"/>
			</svg>
		</svelte:fragment>
		{#if data.verified}
		<div class="p-6 space-y-4 md:space-y-6 sm:p-8 flex justify-center">
			Your email has been successfully verified! You can now login to your account.
		</div>
			<Button href="/login" class="w-full">Proceed to login</Button>
		{:else}
			<div class="p-6 space-y-4 md:space-y-6 sm:p-8 flex justify-center">
			{data.message}
		  </div>
		{/if}
	</Register>
</Section>