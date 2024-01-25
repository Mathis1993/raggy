


class DocumentEmbedder:
    def __init__(self, model_path: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.embedding_model = LangchainEmbedding(HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2'))

    def embed(self, document):
        return self.model.encode(document)