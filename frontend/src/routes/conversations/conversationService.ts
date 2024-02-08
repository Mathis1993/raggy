import {goto, invalidateAll} from "$app/navigation";

const CONVERSATION_API_URL = 'http://localhost:8000/api/conversations/';


export async function createMessage(messageText: string, conversation: Conversation) {
    const message = messageText.trim();
    const response = await fetch(CONVERSATION_API_URL + conversation.id + "/messages/", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({"message": message, "conversation_id": conversation.id}),
    });

    if (!response.ok) {
        console.error('Failed to send message', response);
        return;
    }
    return await response.json();
}


export async function createConversation() {
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

        const data = await response.json();
        await goto(`/conversations/${data.id}`, {replaceState: true});
    } catch (error) {
        console.error('Failed to create conversation', error);
    }
}


export async function retrieveConversation(conversationId: number) {
    try {
        const response = await fetch(CONVERSATION_API_URL + conversationId);

        if (!response.ok) {
            console.error('Failed to retrieve conversation');
            return;
        }

        return await response.json();
    } catch (error) {
        console.error('Failed to retrieve conversation', error);
    }
}


export async function deleteConversation(conversationId: number) {
    try {
        const response = await fetch(CONVERSATION_API_URL + conversationId, {
            method: 'DELETE',
        });

        if (!response.ok) {
            console.error('Failed to delete conversation');
            return;
        }

        console.log('Conversation deleted');
    } catch (error) {
        console.error('Failed to delete conversation', error);
    }
    await goto(`/conversations/`);
    // invalidate page data of layout.svelte
    await invalidateAll();
}