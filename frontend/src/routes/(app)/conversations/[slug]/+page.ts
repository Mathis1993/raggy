import {getMessages, retrieveConversation} from "../conversationService";

export async function load({ fetch, params }) {
    let conversationId = parseInt(params.slug, 10);
    try {
        const conversation: Conversation = await retrieveConversation(conversationId);
        const messages: Message[] = await getMessages(conversationId, 1);

        return { "conversation": conversation, "messages": messages };
    } catch (error) {
        console.error('Error fetching conversation:', error);
        return { status: 500, error };
    }
}
