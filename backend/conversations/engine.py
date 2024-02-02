from typing import List

from llama_index import ServiceContext
from llama_index.agent import ReActAgent
from llama_index.chat_engine import CondensePlusContextChatEngine
from llama_index.core.llms.types import ChatMessage, ChatResponse
from llama_index.llms import OpenAI
from llama_index.memory import ChatMemoryBuffer
from llama_index.tools import QueryEngineTool
from llama_index.vector_stores import MetadataFilters, ExactMatchFilter

from knowledge_base.vector_store import get_index


class ConversationEngine:
    """
    ConversationEngine is the main class for the chatbot. It is responsible for setting up the
    Llamaindex ChatEngine and providing a query method to query the chat engine. It returns a
    response message.
    """

    def __init__(self, conversation_history: List[ChatMessage] = None, model: str = "gpt-3.5-turbo", temperature: float = 0.1):
        self.model = model
        self.temperature = temperature

        self.vector_index = get_index()
        self.conversation_agent = self._build_chat_agent(conversation_history)
        self.conversation_engine = self._build_chat_context_engine(conversation_history)

    def _build_service_context(self) -> ServiceContext:
        return ServiceContext.from_defaults(
            llm=OpenAI(
                model=self.model,
                temperature=self.temperature,
            )
        )

    def _build_chat_agent(self, conversation_history: List[ChatMessage], **kwargs) -> ReActAgent:
        query_engine = self.vector_index.as_query_engine()
        query_engine_tool = QueryEngineTool.from_defaults(query_engine=query_engine)
        chat_agent = ReActAgent.from_tools(
            tools=[query_engine_tool],
            llm=self._build_service_context().llm,
            chat_history=conversation_history,
            verbose=True,
            **kwargs,
        )

        return chat_agent

    def _build_chat_context_engine(self, conversation_history: List[ChatMessage]) -> CondensePlusContextChatEngine:
        # TODO: get user_id from request
        user_id = 1,
        memory = ChatMemoryBuffer.from_defaults(
            token_limit=3900,
            chat_history=conversation_history,
        )
        chat_engine = self.vector_index.as_chat_engine(
            chat_mode="condense_plus_context",
            service_context=self._build_service_context(),
            memory=memory,
            # filters=MetadataFilters(
            #     filters=[
            #         ExactMatchFilter(
            #             key="user_id",
            #             value=user_id,
            #         )
            #     ]
            # ),
        )
        return chat_engine

    def query(self, message: str, use_agent: bool = False) -> ChatResponse:
        if use_agent:
            message = self.conversation_agent.chat(message)
        else:
            message = self.conversation_engine.chat(message)
        return message

