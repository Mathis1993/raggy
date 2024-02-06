<script lang="ts">
    import {Button} from 'flowbite-svelte';
    import {goto, invalidateAll} from "$app/navigation";

    let createConversation = async () => {
        console.log('Creating conversation');
        try {
            const response = await fetch('http://localhost:8000/api/conversations/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
            });

            if (!response.ok) {
                console.error('Failed to create conversation');
                return;
            }

            console.log('Conversation created');

            const data = await response.json();
            await goto(`/conversations/${data.id}`, {replaceState: true});
            await invalidateAll();
        } catch (error) {
            console.error('Failed to create conversation', error);
        }
    }
</script>

<div class="flex items-center justify-center">
    <Button data-sveltekit-reload on:click={createConversation} color="primary" size="lg">Create conversation</Button>
</div>


