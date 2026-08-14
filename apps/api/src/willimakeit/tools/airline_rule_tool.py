from willimakeit.services.airline_rule_service import AirlineRuleService


class AirlineRuleTool:
    def __init__(self, service: AirlineRuleService) -> None:
        self._service = service

    async def search_airline_rules(
        self,
        question: str,
    ) -> str:
        """
        Search the airline knowledge base for airline baggage rules.

        Use this tool whenever the user asks about baggage allowance,
        carry-on baggage, cabin baggage, checked baggage, baggage limits,
        or other airline-specific baggage rules.
        """
        print(f"AIRLINE_TOOL_CALL: {question}")
        results = await self._service.search_rules(
            question=question,
            limit=3,
        )

        if not results:
            return "No relevant airline rules were found."

        return "\n\n".join(
            f"[{result.airline_code} - {result.section}]\n{result.content}"
            for result in results
        )
