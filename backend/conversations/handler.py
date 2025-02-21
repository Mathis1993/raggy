import logging
from typing import List

from django.shortcuts import get_object_or_404
from llama_index.core.base.llms.types import ChatResponse, ChatMessage, MessageRole

from conversations.exceptions import ChatEngineError, ConversationError, PersistenceError
from conversations.engine import (
    LlamaIndexChatEngine,
)
from conversations.models import Conversation
from knowledge_base.vector_store import vector_store

logger = logging.getLogger(__name__)



class ConversationHandler:
    def __init__(self, conversation_id: int, chat_engine_cls=LlamaIndexChatEngine):
        self.conversation = get_object_or_404(Conversation, id=conversation_id)
        self.chat_engine_cls = chat_engine_cls
        self._initialize_chat_engine()

    def _initialize_chat_engine(self):
        conversation_history = self._get_conversation_history()
        self.chat_engine = self.chat_engine_cls(
            vector_store=vector_store,  # This should be injected
            user_id=self.conversation.user.id,
            conversation_history=conversation_history,
        )

    def handle_message(self, user_message: str, add_to_conversation: bool = True) -> ChatMessage:
        try:
            if add_to_conversation:
                self._persist_user_message(user_message)
                self.conversation.mark_as_running()

            assistant_response = self._process_message(user_message)
            return self._persist_assistant_response(assistant_response)

        except ChatEngineError as e:
            logger.error(f"Chat engine error: {e}")
            self.conversation.mark_as_failed()
            raise
        except PersistenceError as e:
            logger.error(f"Database persistence error: {e}")
            self.conversation.mark_as_failed()
            raise
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            self.conversation.mark_as_failed()
            raise ConversationError(f"Unexpected error during message handling: {e}")

    def _process_message(self, user_message: str) -> ChatResponse:
        try:
            return self.chat_engine.query(user_message)
        except Exception as e:
            raise ChatEngineError(f"Error processing message: {e}")

    def _persist_assistant_response(self, response: ChatResponse) -> ChatMessage:
        try:
            message_object = self.conversation.add_assistant_message(response.response)
            message_object.add_sources(response.source_nodes)
            self.conversation.mark_as_completed()
            return message_object
        except Exception as e:
            raise PersistenceError(f"Error persisting assistant response: {e}")

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
