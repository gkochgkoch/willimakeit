from willimakeit.schemas.connection import (
    ConnectionAssessment,
    ConnectionAssessmentRequest,
    ConnectionRisk,
)


class ConnectionService:
    def assess(
        self,
        req: ConnectionAssessmentRequest,
    ) -> ConnectionAssessment:
        available_minutes = int(
            (req.outbound_departure - req.inbound_arrival).total_seconds() // 60
        )

        required_minutes = (
            req.minimum_connection_minutes
            + req.terminal_transfer_minutes
            + req.security_check_minutes
            + req.immigration_control_minutes
            + req.disruption_buffer_minutes
        )

        margin_minutes = available_minutes - required_minutes
        reasons: list[str] = []

        if available_minutes < 0:
            risk = ConnectionRisk.IMPOSSIBLE
            reasons.append(
                "The outbound flight departs before the inbound flight arrives."
            )
        elif margin_minutes < 0:
            risk = ConnectionRisk.HIGH
            reasons.append(
                "The available connection is shorter than the required time."
            )
        elif margin_minutes < 20:
            risk = ConnectionRisk.HIGH
            reasons.append("The connection has less than 20 minutes of contingency.")
        elif margin_minutes < 45:
            risk = ConnectionRisk.MODERATE
            reasons.append("The connection has limited contingency for delays.")
        else:
            risk = ConnectionRisk.LOW
            reasons.append("The connection has a reasonable time buffer.")

        return ConnectionAssessment(
            available_minutes=available_minutes,
            required_minutes=required_minutes,
            margin_minutes=margin_minutes,
            risk=risk,
            reasons=reasons,
        )
