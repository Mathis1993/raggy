from typing import List

from django.shortcuts import get_object_or_404
from llama_index.core.llms.types import ChatResponse, ChatMessage, MessageRole

from conversations.engine import ConversationEngine
from conversations.models import Conversation, Message


class ConversationHandler:
    """
    Class responsible for handling the conversation. It is responsible for creating a conversation
    engine and  handling the messages from the user and the assistant. It stores the messages in
    the database.
    """
    def __init__(self, conversation_id: int):
        self.conversation = get_object_or_404(Conversation, id=conversation_id)
        self.conversation_history = self._get_conversation_history()
        self.conversation_engine = ConversationEngine(
            conversation_history=self.conversation_history,
        )

    def handle_message(self, user_message: str):
        self.conversation.add_user_message(user_message)
        assistant_response: ChatResponse = self.conversation_engine.query(user_message)
        response_msg_obj = self.conversation.add_assistant_message(assistant_response.response)
        return response_msg_obj

    def _get_conversation_history(self) -> List[ChatMessage]:
        if self.conversation is None:
            return []

        previous_messages = self.conversation.get_message_history()
        conversation_history = [
            ChatMessage(
                role=MessageRole.USER if message.is_user_message else MessageRole.ASSISTANT,
                content=message.text,
            ) for message in previous_messages
        ]
        return conversation_history
