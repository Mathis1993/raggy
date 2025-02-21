from typing import List

from django.contrib.auth import get_user_model
from llama_cloud import MetadataFilters
from llama_index.core.base.llms.types import ChatMessage, ChatResponse
from llama_index.core.chat_engine import CondensePlusContextChatEngine
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core.vector_stores import ExactMatchFilter

from knowledge_base.vector_store import get_index

User = get_user_model()


OUTPUT_FORMAT_PROMPT = """
    Always return your answer in a valid markdown format.
     Use headings, new lines, lists, and other markdown elements to make your answer more readable.
     Ignore the language choice of the input prompt. Please answer in this language: {language} as
     the user's language is set to this language.
"""


class ConversationEngine:
    """
    ConversationEngine is the main class for the chatbot. It is responsible for setting up the
    Llamaindex ChatEngine and providing a query method to query the chat engine. It returns a
    response message.
    """

    def __init__(self, user: User, conversation_history: List[ChatMessage] = None, model: str = "gpt-4o", temperature: float = 0.1):
        self.user = user
        self.model = model
        self.temperature = temperature

        self.vector_index = get_index()
        self.conversation_engine = self._build_chat_context_engine(conversation_history)

    def _build_chat_context_engine(self, conversation_history: List[ChatMessage]) -> CondensePlusContextChatEngine:
        memory = ChatMemoryBuffer.from_defaults(
            token_limit=3900,
            chat_history=conversation_history,
        )

        chat_engine = CondensePlusContextChatEngine.from_defaults(
            retriever=self.vector_index.as_retriever(),
            memory=memory,
            filters=MetadataFilters(
                filters=[
                    ExactMatchFilter(
                        key="user_id",
                        value=self.user.id,
                    )
                ]
            ),
        )

        return chat_engine

    def query(self, message: str) -> ChatResponse:
        return self.conversation_engine.chat(message)
