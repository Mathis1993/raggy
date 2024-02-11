<script lang="ts">
    import {Button} from 'flowbite-svelte';
    import {createConversation} from "./conversations/conversationService";
</script>

<div class="flex h-full items-center justify-center">
    <Button data-sveltekit-reload on:click={createConversation} color="primary" size="lg">Create conversation</Button>
</div>


