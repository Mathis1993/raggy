import {retrieveConversations} from "./conversations/conversationService";

export const ssr = false;

/** @type {import('../../../.svelte-kit/types/src/routes').PageLoad} */
export async function load({ fetch }) {
    const conversations = await retrieveConversations(1)
    const userResponse = await fetch('http://127.0.0.1:8000/users/info/', {credentials: 'include'});
    const user: User = await userResponse.json()
    return {"conversations": conversations, "user": user, "conversationsLoaded": true, "page": 1}
}