<script lang="ts">
    import { writable } from 'svelte/store';
    import { Button, Helper, Input, Label } from 'flowbite-svelte';
    import { goto } from '$app/navigation';
    import {signUp} from "../authService";
    import {Register, Section} from "flowbite-svelte-blocks";
    import {addToast} from "../../../stores/toastStore";

    // Initialize error messages as arrays to handle multiple messages
    const emailError = writable([]);
    const password1Error = writable([]);
    const password2Error = writable([]);

    async function handleSubmit(event) {
        const form = event.target;
        const formData = new FormData(form);

        const signUpData = {
            email: formData.get('email'),
            password1: formData.get('password1'),
            password2: formData.get('password2'),
            first_name: formData.get('first_name'),
            last_name: formData.get('last_name'),
        };

        try {
            await signUp(signUpData);
            addToast('Account created successfully', 'success');
            await goto('/login');
        } catch (error) {
            addToast('Failed to create account', 'error');
            emailError.set(error.email || []);
            password1Error.set(error.password1 || []);
            password2Error.set(error.password2 || []);
        }
    }
</script>

<Section name="register" sectionClass="lg:w-1/2 w-full">
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
                <h3 class="text-xl font-medium text-gray-900 dark:text-white p-0">Sign Up</h3>
                <Label class="space-y-2">
                    <span>Your email</span>
                    <Input type="email" autocomplete="email" name="email" placeholder="name@mail.com" required/>
                    {#if $emailError.length}
                        {#each $emailError as error}
                            <Helper color="red">{error}</Helper>
                        {/each}
                    {/if}
                </Label>
                <Label class="space-y-2">
                    <span>Your first name</span>
                    <Input type="text" autocomplete="given-name" name="first_name" placeholder="John"/>
                </Label>
                <Label class="space-y-2">
                    <span>Your last name</span>
                    <Input type="text" autocomplete="family-name" name="last_name" placeholder="Doe"/>
                </Label>
                <Label class="space-y-2">
                    <span>Your password</span>
                    <Input type="password" autocomplete="current-password" name="password1" placeholder="•••••" required/>
                    {#if $password1Error.length}
                        {#each $password1Error as error}
                            <Helper color="red">{error}</Helper>
                        {/each}
                    {/if}
                </Label>
                <Label class="space-y-2">
                    <span>Confirm password</span>
                    <Input type="password" autocomplete="confirm-password" name="password2" placeholder="•••••" required/>
                    {#if $password2Error.length}
                        {#each $password2Error as error}
                            <Helper color="red">{error}</Helper>
                        {/each}
                    {/if}
                </Label>
                <!--				<div class="flex items-start">-->
                <!--					<Checkbox>I accept the <a class="font-medium text-primary-600 hover:underline dark:text-primary-500" href="/"> Terms and Conditions</a></Checkbox>-->
                <!--				</div>-->
                <Button type="submit" class="w-full1">Sign up</Button>
                <div class="text-sm font-medium text-gray-500 dark:text-gray-300">
                    Already have an account? <a href="/login"
                                                class="font-medium text-primary-600 hover:underline dark:text-primary-500">Sign
                    in here</a>
                </div>
            </form>
        </div>
    </Register>
</Section>