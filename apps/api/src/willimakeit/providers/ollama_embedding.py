from agent_framework_ollama import OllamaEmbeddingClient


class OllamaEmbeddingProvider:
    def __init__(
        self,
        client: OllamaEmbeddingClient,
        model: str,
    ):
        self._client = client
        self._model = model

    async def embed(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        result = await self._client.get_embeddings(
            texts,
            options={
                "model": self._model,
            },
        )

        return [embedding.vector for embedding in result]
