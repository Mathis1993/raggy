import {goto, invalidateAll} from "$app/navigation";
import {getCsrfToken} from '$lib/cookies';

const CONVERSATION_API_URL = 'http://127.0.0.1:8000/api/conversations/';


export async function createMessage(messageText: string, conversation: Conversation) {
    const message = messageText.trim();
    const response = await fetch(CONVERSATION_API_URL + conversation.id + "/messages/", {
        method: 'POST',
        credentials: 'include',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfToken(),
        },
        body: JSON.stringify({"message": message, "conversation_id": conversation.id}),
    });

    if (!response.ok) {
        console.error('Failed to send message', response);
        return;
    }
    return await response.json();
}


export async function getMessages(conversationId: number, page: number = 1) {
    let queryParams = new URLSearchParams();
    queryParams.append('page', page.toString());
    const messageResponse = await fetch(CONVERSATION_API_URL + conversationId + "/messages/?" + queryParams.toString(), {credentials: 'include'});
    if (!messageResponse.ok) {
        console.error("Failed to fetch messages", messageResponse.status);
        return [];
    }
    let messages = await messageResponse.json();
    messages.page = page;
    return messages;
}


export async function retrieveConversations(page: number = 1) {
    let queryParams = new URLSearchParams();
    queryParams.append('page', page.toString());
    const response = await fetch(CONVERSATION_API_URL + "?" + queryParams.toString(), {credentials: 'include'});
    if (!response.ok) {
        console.error("Failed to fetch conversations", response.status);
        return [];
    }
    let conversations = await response.json();
    conversations.page = page;
    return conversations;
}


export async function createConversation() {
    try {
        const response = await fetch('http://127.0.0.1:8000/api/conversations/', {
            method: 'POST',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken(),
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
        const response = await fetch(CONVERSATION_API_URL + conversationId, {credentials: 'include'});

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
            credentials: 'include',
            headers: {
                'X-CSRFToken': getCsrfToken(),
            },
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