<script lang="ts">
    import { writable } from 'svelte/store';
    import { Button, Input, Label } from 'flowbite-svelte';
    import { goto } from '$app/navigation';
    import { Register, Section } from 'flowbite-svelte-blocks';
    import { login } from '../authService';
    import {addToast} from "../../../stores/toastStore"; // Adjust the path as necessary
    import { Banner } from "flowbite-svelte-blocks";
    import { CloseButton } from "flowbite-svelte";
    import { visible, visibleText } from '../../../stores/visibleStore';

    let email = '';
    let password = '';
    let loginError = writable('');

    async function handleSubmit(event) {
        event.preventDefault();

        try {
            await login(email, password);
            addToast('You have been logged in.', 'success')
            await goto('/');
        } catch (error) {
            addToast('An error occurred during login.', 'error')
            loginError.set(error.message || 'An error occurred during login.');
        }
    }
</script>

<Section name="login" sectionClass="w-1/2">
    {#if $visible}
        <!-- ToDo (ME-2024-02-14): Make the popup look nicer -->
        <Banner>
            <p class="text-m font-bold text-gray-500 dark:text-gray-400">
                {$visibleText}
            </p>
            <CloseButton on:click={() => ($visible = false)} class="text-gray-400 hover:bg-gray-200 hover:text-gray-900 rounded-lg text-sm p-1.5 dark:hover:bg-gray-600 dark:hover:text-white" />
        </Banner>
    {/if}
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
                <h3 class="text-xl font-medium text-gray-900 dark:text-white p-0">Sign In</h3>
                <Label class="space-y-2">
                    <span>Your email</span>
                    <Input bind:value={email} autocomplete="email" type="email" name="email" placeholder="name@company.com" required/>
                </Label>
                <Label class="space-y-2">
                    <span>Your password</span>
                    <Input bind:value={password} autocomplete="current-password" type="password" name="password" placeholder="•••••" required/>
                </Label>
                {#if $loginError}
                    <p class="text-red-500">{ $loginError }</p>
                {/if}
                <div class="flex items-start">
                    <a href="/reset-password" class="ml-auto text-sm text-blue-700 hover:underline dark:text-blue-500">Forgot
                        password?</a>
                </div>
                <Button type="submit" class="w-full1">Sign in</Button>
                <p class="text-sm font-light text-gray-500 dark:text-gray-400">
                    Don’t have an account yet? <a href="/signup"
                                                  class="font-medium text-primary-600 hover:underline dark:text-primary-500">Sign
                    up</a>
                </p>
            </form>
        </div>
    </Register>
</Section>
