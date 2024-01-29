from llama_index import ServiceContext
from llama_index.agent import ReActAgent
from llama_index.core.llms.types import MessageRole, ChatMessage
from llama_index.llms import OpenAI
from llama_index.tools import QueryEngineTool

from generation.models import Conversation
from retrieval.tools.index import DocumentIndex


class ChatEngine:

    def __init__(self, conversation: Conversation = None, user_id: int = 1, model: str = "gpt-3.5-turbo", temperature: float = 0.1):
        self.conversation = conversation
        self.model = model
        self.temperature = temperature
        self.user_id = user_id

        self.vector_index = DocumentIndex().index
        self.chat_agent = self._build_chat_agent()

    def _build_service_context(self):
        return ServiceContext.from_defaults(
            llm=OpenAI(
                model=self.model,
                temperature=self.temperature,
            )
        )

    def _build_chat_agent(self, **kwargs):
        query_engine = self.vector_index.as_query_engine()

        query_engine_tool = QueryEngineTool.from_defaults(query_engine=query_engine)

        chat_agent = ReActAgent.from_tools(
            tools=[query_engine_tool],
            llm=self._build_service_context().llm,
            chat_history=self._build_chat_history(),
            verbose=True,
            **kwargs,
        )

        return chat_agent

    def _build_chat_history(self):
        if self.conversation is None:
            return []

        previous_messages = self.conversation.get_message_history()
        custom_chat_history = [
            ChatMessage(
                role=MessageRole.USER if message.is_user_message else MessageRole.ASSISTANT,
                content=message.text,
            ) for message in previous_messages
        ]
        return custom_chat_history

    def query(self, message: str):
        message = self.chat_agent.chat(message)
        return message

