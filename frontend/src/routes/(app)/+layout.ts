import { retrieveConversations } from "./conversations/conversationService";
import { fetchFromBackend } from "$lib/fetch";

export const ssr = false;

/** @type {import('../../../.svelte-kit/types/src/routes').PageLoad} */
export async function load() {
  const conversations = await retrieveConversations(1);
  const userResponse = await fetchFromBackend(
    "http://127.0.0.1:8000/users/info/",
  );
  const user: User = await userResponse.json();
  return {
    conversations: conversations,
    user: user,
    conversationsLoaded: true,
    page: 1,
  };
}
