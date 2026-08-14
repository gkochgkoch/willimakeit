from willimakeit.providers.base import EmbeddingProvider
from willimakeit.schemas.rag_pipeline import AirlineRuleChunk


class EmbeddingService:
    def __init__(self, provider: EmbeddingProvider):
        self._provider = provider

    async def embed_texts(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        return await self._provider.embed(texts)

    async def embed_chunks(
        self,
        chunks: list[AirlineRuleChunk],
    ) -> list[list[float]]:
        texts = [chunk.content for chunk in chunks]

        return await self._provider.embed(texts)
