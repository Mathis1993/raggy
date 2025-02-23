import { goto, invalidateAll } from "$app/navigation";
import { fetchFromBackend } from "$lib/fetch";
import type { Conversation } from "../../../types/conversation";

const CONVERSATION_API_URL = "http://127.0.0.1:8000/api/conversations/";

export async function createMessage(
  messageText: string,
  conversation: Conversation,
) {
  const message = messageText.trim();
  const response = await fetchFromBackend(
    CONVERSATION_API_URL + conversation.id + "/messages/",
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        message: message,
        conversation_id: conversation.id,
      }),
    },
  );

  if (!response.ok) {
    console.error("Failed to send message", response);
    return;
  }
  return await response.json();
}

export async function getMessages(conversationId: number, page: number = 1) {
  let queryParams = new URLSearchParams();
  queryParams.append("page", page.toString());
  const messageResponse = await fetchFromBackend(
    CONVERSATION_API_URL +
      conversationId +
      "/messages/?" +
      queryParams.toString(),
  );
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
  queryParams.append("page", page.toString());
  const response = await fetchFromBackend(
    CONVERSATION_API_URL + "?" + queryParams.toString(),
  );
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
    const response = await fetchFromBackend(
      "http://127.0.0.1:8000/api/conversations/",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({}),
      },
    );

    if (!response.ok) {
      console.log(response);
      console.error("Failed to create conversation");
      return;
    }

    const data = await response.json();
    await goto(`/conversations/${data.id}`, { replaceState: true });
  } catch (error) {
    console.error("Failed to create conversation", error);
  }
}

export async function retrieveConversation(conversationId: number) {
  try {
    const response = await fetchFromBackend(
      CONVERSATION_API_URL + conversationId,
    );

    if (!response.ok) {
      console.error("Failed to retrieve conversation");
      return;
    }

    return await response.json();
  } catch (error) {
    console.error("Failed to retrieve conversation", error);
  }
}

export async function deleteConversation(conversationId: number) {
  try {
    const response = await fetchFromBackend(
      CONVERSATION_API_URL + conversationId + "/",
      {
        method: "DELETE",
      },
    );

    if (!response.ok) {
      console.error("Failed to delete conversation");
      return;
    }

    console.log("Conversation deleted");
  } catch (error) {
    console.error("Failed to delete conversation", error);
  }
  await goto(`/conversations/`);
  // invalidate page data of layout.svelte
  await invalidateAll();
}

export async function createConversationWithMessage(messageText: string) {
  try {
    const response = await fetchFromBackend(
      CONVERSATION_API_URL,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({}),
      },
    );

    if (!response.ok) {
      console.error("Failed to create conversation");
      return;
    }

    const conversation = await response.json();

    // Send the initial message
    await createMessage(messageText, conversation);

    // Navigate to the new conversation
    await goto(`/conversations/${conversation.id}`, { replaceState: true });

    return conversation;
  } catch (error) {
    console.error("Failed to create conversation with message", error);
  }
}
