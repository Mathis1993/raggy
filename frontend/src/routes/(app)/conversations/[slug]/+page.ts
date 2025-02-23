import type { Message } from "postcss";
import type { Conversation } from "../../../../types/conversation";
import { getMessages, retrieveConversation } from "../conversationService";

export const ssr = false;

export async function load({ params, url }) {
  let conversationId = parseInt(params.slug, 10);
  try {
    const conversation: Conversation =
      await retrieveConversation(conversationId);
    const messages: Message[] = await getMessages(conversationId, 1);

    return {
      conversation: conversation,
      messages: messages,
      fromHistory: url.searchParams.has('fromHistory')
    };
  } catch (error) {
    console.error("Error fetching conversation:", error);
    return { status: 500, error };
  }
}
