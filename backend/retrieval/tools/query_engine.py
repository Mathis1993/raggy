from llama_index import ServiceContext
from openai import OpenAI

from retrieval.tools.index import DocumentIndex


class QueryEngine:

    def __init__(self, model: str = "text-davinci-002", temperature: float = 0.1):
        self.temperature = temperature
        self.model = model
        self.service_context = self._build_service_context()
        self.index = DocumentIndex().get_index()

    def _build_service_context(self):
        return ServiceContext.from_defaults(
            llm=OpenAI(
                model=self.model,
                temperature=self.temperature,
            ),
            system_prompt="You are an AI assistant answering questions related to websites."
        )

    def query(self, question: str):
        query_engine = self.index.as_query_engine(service_context=self.service_context)
        return query_engine.query(question)
