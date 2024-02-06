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
    console.log('Redirecting to /conversations/');
    await goto(`/conversations/`, {replaceState: true});
    await invalidateAll();
}