from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from willimakeit.db.models.airport_transfer_rule import AirportTransferRule


class AirportTransferRuleRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def find_rule(
        self,
        airport_code: str,
        arrival_terminal: str,
        departure_terminal: str,
        self_transfer: bool,
    ) -> AirportTransferRule | None:
        statement = select(AirportTransferRule).where(
            AirportTransferRule.airport_code == airport_code.upper(),
            AirportTransferRule.arrival_terminal == arrival_terminal,
            AirportTransferRule.departure_terminal == departure_terminal,
            AirportTransferRule.self_transfer == self_transfer,
        )
        return await self._session.scalar(statement)
