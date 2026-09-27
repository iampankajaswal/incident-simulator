from api.models import Incident, RCAResult


def analyze_incident(incident: Incident) -> RCAResult:
    """
    Generate a deterministic RCA from incident evidence.

    This is intentionally rules-based for Milestone 1.
    AI-assisted RCA will be introduced later.
    """

    if incident.scenario == "high-cpu":
        return RCAResult(
            root_cause="CPU saturation caused by simulated CPU-intensive workload.",
            evidence=[
                "HighCPU alert was generated.",
                "The high-cpu fault injection scenario was active.",
                f"CPU stress ran with service '{incident.service}'.",
            ],
            impact="The service may experience increased latency or reduced request capacity.",
            recommendation=(
                "Investigate CPU-intensive workloads, review CPU requests and limits, "
                "and validate horizontal scaling configuration."
            ),
        )

    return RCAResult(
        root_cause="Unknown",
        evidence=[
            "No RCA rule matched the incident scenario.",
        ],
        impact="Unknown",
        recommendation="Investigate the incident manually.",
    )
