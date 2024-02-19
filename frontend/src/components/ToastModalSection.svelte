<script lang="ts">
    import { toasts } from "../stores/toastStore.ts";
    import ToastModal from "./ToastModal.svelte";
</script>

{#if $toasts}
    <section class="absolute top-20 right-10 z-50">
        {#each $toasts as toast (toast.id)}
            <ToastModal {toast} />
        {/each}
    </section>
{/if}
