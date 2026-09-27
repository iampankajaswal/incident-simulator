from api.models import Alert
from controller.incident_controller import IncidentController


def test_incident_lifecycle():
    controller = IncidentController()

    alert = Alert(
        alert_name="HighCPU",
        severity="SEV-2",
        scenario="high-cpu",
        service="incident-simulator",
    )

    incident = controller.create_incident(alert)

    assert incident.id == "INC-00001"
    assert incident.status == "INVESTIGATING"
    assert len(incident.alerts) == 1
    assert len(incident.timeline) == 2

    controller.run_rca(incident.id)

    assert incident.rca is not None
    assert incident.status == "MITIGATED"

    controller.resolve_incident(incident.id)

    assert incident.status == "RESOLVED"
    assert incident.resolved_at is not None

    assert len(incident.timeline) == 6

    event_types = [
        event.event_type
        for event in incident.timeline
    ]

    assert event_types == [
        "INCIDENT_CREATED",
        "INVESTIGATION_STARTED",
        "RCA_STARTED",
        "RCA_COMPLETED",
        "MITIGATED",
        "RESOLVED",
    ]
