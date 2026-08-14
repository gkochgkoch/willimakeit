from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from willimakeit.db.models.airline_rule_chunks import AirlineRuleChunkModel
from willimakeit.schemas.rag_pipeline import AirlineRuleChunk


class AirlineRuleRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def insert_chunks(
        self,
        chunks: list[AirlineRuleChunk],
        embeddings: list[list[float]],
    ) -> None:
        if len(chunks) != len(embeddings):
            raise ValueError("Chunks and embeddings must have the same length")

        rows = [
            {
                "airline_code": chunk.airline_code,
                "content": chunk.content,
                "section": chunk.section,
                "effective_date": chunk.effective_date,
                "embedding": embedding,
            }
            for chunk, embedding in zip(chunks, embeddings, strict=True)
        ]

        statement = insert(AirlineRuleChunkModel).values(rows)

        await self._session.execute(statement)
        await self._session.commit()

    async def search(
        self,
        embedding: list[float],
        airline_code: str | None = None,
        limit: int = 3,
    ) -> list[AirlineRuleChunkModel]:
        distance = AirlineRuleChunkModel.embedding.cosine_distance(embedding)

        statement = select(AirlineRuleChunkModel)

        if airline_code is not None:
            statement = statement.where(
                AirlineRuleChunkModel.airline_code == airline_code
            )

        statement = statement.order_by(distance).limit(limit)

        result = await self._session.scalars(statement)

        return list(result.all())
