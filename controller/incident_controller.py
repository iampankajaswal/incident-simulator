#from datetime import datetime, timezone
from datetime import UTC, datetime

from api.models import Alert, Incident
from controller.rca_engine import analyze_incident
from controller.timeline import add_event


class IncidentController:
    def __init__(self) -> None:
        self._incidents: dict[str, Incident] = {}
        self._counter = 0

    def _generate_incident_id(self) -> str:
        self._counter += 1
        return f"INC-{self._counter:05d}"

    def create_incident(self, alert: Alert) -> Incident:
        incident_id = self._generate_incident_id()

        incident = Incident(
            id=incident_id,
            title=f"{alert.alert_name} detected",
            severity=alert.severity,
            status="OPEN",
            scenario=alert.scenario,
            service=alert.service,
            alerts=[alert],
        )

        self._incidents[incident.id] = incident

        add_event(
            incident,
            "INCIDENT_CREATED",
            f"Incident {incident.id} created from alert {alert.alert_name}.",
        )

        incident.status = "INVESTIGATING"

        add_event(
            incident,
            "INVESTIGATION_STARTED",
            "Incident investigation started.",
        )

        return incident

    def run_rca(self, incident_id: str) -> Incident:
        incident = self.get_incident(incident_id)

        add_event(
            incident,
            "RCA_STARTED",
            "Root cause analysis started.",
        )

        incident.rca = analyze_incident(incident)

        add_event(
            incident,
            "RCA_COMPLETED",
            f"Root cause identified: {incident.rca.root_cause}",
        )

        incident.status = "MITIGATED"

        add_event(
            incident,
            "MITIGATED",
            "Incident mitigation completed.",
        )

        return incident

    def resolve_incident(self, incident_id: str) -> Incident:
        incident = self.get_incident(incident_id)

        incident.status = "RESOLVED"
        #incident.resolved_at = datetime.now(timezone.utc)
        incident.resolved_at = datetime.now(UTC)

        add_event(
            incident,
            "RESOLVED",
            "Incident resolved.",
        )

        return incident

    def get_incident(self, incident_id: str) -> Incident:
        incident = self._incidents.get(incident_id)

        if incident is None:
            raise KeyError(f"Incident {incident_id} not found")

        return incident

    def list_incidents(self) -> list[Incident]:
        return list(self._incidents.values())
