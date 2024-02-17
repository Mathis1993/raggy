<script>
    import { Toast } from 'flowbite-svelte';
    import { blur } from 'svelte/transition';
    import { BellOutline } from 'flowbite-svelte-icons';
    import {dismissToast, toasts} from "../stores/toastStore.ts";

    const autoHideTime = 5000; // 5 seconds
</script>

{#if $toasts}
    <section class="absolute top-20 right-10 z-50">
        {#each $toasts as toast (toast.id)}
            <Toast transition={blur} color="purple" class="mb-4 z-0">
                <BellOutline slot="icon" class="w-5 h-5 text-primary-500 bg-primary-100 dark:bg-primary-800 dark:text-primary-200" />
                {toast.message}
                {#if toast.dismissable}
                    {setTimeout(() => dismissToast(toast.id), autoHideTime)}
                {/if}
            </Toast>
        {/each}
    </section>
{/if}
