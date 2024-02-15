from typing import List

from django.contrib.auth import get_user_model
from llama_index import ServiceContext
from llama_index.chat_engine import CondensePlusContextChatEngine
from llama_index.core.llms.types import ChatMessage, ChatResponse
from llama_index.llms import OpenAI
from llama_index.memory import ChatMemoryBuffer
from llama_index.vector_stores import MetadataFilters, ExactMatchFilter

from knowledge_base.vector_store import get_index

User = get_user_model()


OUTPUT_FORMAT_PROMPT = """
    Always return your answer in a valid markdown format.
     Use headings, new lines, lists, and other markdown elements to make your answer more readable.
"""


class ConversationEngine:
    """
    ConversationEngine is the main class for the chatbot. It is responsible for setting up the
    Llamaindex ChatEngine and providing a query method to query the chat engine. It returns a
    response message.
    """

    def __init__(self, user: User, conversation_history: List[ChatMessage] = None, model: str = "gpt-3.5-turbo", temperature: float = 0.1):
        self.user = user
        self.model = model
        self.temperature = temperature

        self.vector_index = get_index()
        self.conversation_engine = self._build_chat_context_engine(conversation_history)

    def _build_service_context(self) -> ServiceContext:
        return ServiceContext.from_defaults(
            llm=OpenAI(
                model=self.model,
                temperature=self.temperature,
                system_prompt=OUTPUT_FORMAT_PROMPT,
            )
        )

    def _build_chat_context_engine(self, conversation_history: List[ChatMessage]) -> CondensePlusContextChatEngine:
        memory = ChatMemoryBuffer.from_defaults(
            token_limit=3900,
            chat_history=conversation_history,
        )

        chat_engine = CondensePlusContextChatEngine.from_defaults(
            retriever=self.vector_index.as_retriever(),
            service_context=self._build_service_context(),
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
