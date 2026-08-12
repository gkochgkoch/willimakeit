from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from willimakeit.repositories.airport_transfer_rule_repository import (
    AirportTransferRuleRepository,
)
from willimakeit.schemas.airport_transfer import AirportTransferEstimate


class AirportTransferRuleNotFoundError(Exception):
    pass


class AirportTransferService:
    def __init__(
        self,
        session_factory: async_sessionmaker[AsyncSession],
    ) -> None:
        self._session_factory = session_factory

    async def estimate_transfer(
        self,
        airport_code: str,
        arrival_terminal: str,
        departure_terminal: str,
        self_transfer: bool,
    ) -> AirportTransferEstimate:
        async with self._session_factory() as session:
            repository = AirportTransferRuleRepository(session)
            rule = await repository.find_rule(
                airport_code=airport_code,
                arrival_terminal=arrival_terminal,
                departure_terminal=departure_terminal,
                self_transfer=self_transfer,
            )

            if rule is None:
                airport_code = airport_code.upper()
                raise AirportTransferRuleNotFoundError(
                    f"No transfer rule exists for {airport_code} "
                    f"from terminal {arrival_terminal} to terminal {departure_terminal}"
                )

            total_required_minutes = (
                rule.terminal_transfer_minutes
                + rule.security_minutes
                + rule.immigration_minutes
                + rule.baggage_recheck_minutes
            )

            return AirportTransferEstimate(
                airport_code=rule.airport_code,
                arrival_terminal=rule.arrival_terminal,
                departure_terminal=rule.departure_terminal,
                terminal_transfer_minutes=rule.terminal_transfer_minutes,
                security_minutes=rule.security_minutes,
                immigration_minutes=rule.immigration_minutes,
                baggage_recheck_minutes=rule.baggage_recheck_minutes,
                total_required_minutes=total_required_minutes,
                self_transfer=rule.self_transfer,
                confidence=rule.confidence,
            )
