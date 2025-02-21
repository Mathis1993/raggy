from typing import List
from abc import ABC, abstractmethod
import logging

from django.contrib.auth import get_user_model
from llama_cloud import MetadataFilters
from llama_index.core.base.llms.types import ChatMessage, ChatResponse
from llama_index.core.chat_engine import CondensePlusContextChatEngine
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core.vector_stores import ExactMatchFilter

from knowledge_base.vector_store import vector_store

logger = logging.getLogger(__name__)

User = get_user_model()

OUTPUT_FORMAT_PROMPT = """
    Always return your answer in a valid markdown format.
     Use headings, new lines, lists, and other markdown elements to make your answer more readable.
     Ignore the language choice of the input prompt. Please answer in this language: {language} as
     the user's language is set to this language.
"""


class BaseChatEngine(ABC):
    @abstractmethod
    def query(self, message: str) -> ChatResponse:
        pass


class LlamaIndexChatEngine(BaseChatEngine):
    def __init__(
        self,
        user_id: int,
        conversation_history: List[ChatMessage] = None,
        model: str = "gpt-4o",
        temperature: float = 0.1,
    ):
        self.vector_store = vector_store
        self.user_id = user_id
        self.model = model
        self.temperature = temperature
        self.conversation_engine = self._build_chat_context_engine(conversation_history)

    def query(self, message: str) -> ChatResponse:
        return self.conversation_engine.chat(message)

    def _build_chat_context_engine(
        self, conversation_history: List[ChatMessage]
    ) -> CondensePlusContextChatEngine:
        memory = ChatMemoryBuffer.from_defaults(
            token_limit=3900,
            chat_history=conversation_history,
        )

        chat_engine = CondensePlusContextChatEngine.from_defaults(
            retriever=self.vector_store.get_index().as_retriever(),
            memory=memory,
            filters=MetadataFilters(
                filters=[
                    ExactMatchFilter(
                        key="user_id",
                        value=self.user_id,
                    )
                ]
            ),
        )

        return chat_engine
