from willimakeit.repositories.airline_rule_repository import (
    AirlineRuleRepository,
)
from willimakeit.services.embedding_service import EmbeddingService


class AirlineRuleService:
    def __init__(
        self,
        embedding_service: EmbeddingService,
        session_factory,
    ) -> None:
        self._embedding_service = embedding_service
        self._session_factory = session_factory

    async def search_rules(
        self,
        question: str,
        limit: int = 3,
    ):
        embeddings = await self._embedding_service.embed_texts([question])
        query_embedding = embeddings[0]

        async with self._session_factory() as session:
            repository = AirlineRuleRepository(session)

            return await repository.search(
                embedding=query_embedding,
                limit=limit,
            )
