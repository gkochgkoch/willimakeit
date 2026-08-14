import asyncio

from agent_framework.ollama import OllamaEmbeddingClient

from willimakeit.config import settings
from willimakeit.db.session import async_session_factory
from willimakeit.providers.ollama_embedding import OllamaEmbeddingProvider
from willimakeit.rag.sample_airline_rules import AIRLINE_RULES
from willimakeit.repositories.airline_rule_repository import AirlineRuleRepository
from willimakeit.services.embedding_service import EmbeddingService


async def main() -> None:
    ollama_client = OllamaEmbeddingClient(
        host=settings.ollama_host,
        model=settings.embedding_model,
    )

    embedding_provider = OllamaEmbeddingProvider(
        client=ollama_client,
        model=settings.embedding_model,
    )

    embedding_service = EmbeddingService(
        provider=embedding_provider,
    )

    embeddings = await embedding_service.embed_chunks(AIRLINE_RULES)

    async with async_session_factory() as session:
        repository = AirlineRuleRepository(session)

        await repository.insert_chunks(
            AIRLINE_RULES,
            embeddings,
        )

    print(f"Inserted {len(AIRLINE_RULES)} airline rule chunks")


if __name__ == "__main__":
    asyncio.run(main())
