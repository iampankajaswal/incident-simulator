from datetime import UTC, datetime
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import ValidationError

from api.models import Alert
from controller.dependencies import incident_controller

router = APIRouter(prefix="/webhooks", tags=["webhooks"])

VALID_SEVERITIES = {"SEV-1", "SEV-2", "SEV-3", "SEV-4"}


def _find_active_incident(
    alert_name: str,
    scenario: str,
    service: str,
):
    """Find an existing, unresolved incident for this alert."""
    for incident in reversed(incident_controller.list_incidents()):
        if (
            incident.status != "RESOLVED"
            and incident.scenario == scenario
            and incident.service == service
            and any(
                item.alert_name == alert_name
                for item in incident.alerts
            )
        ):
            return incident
    return None


@router.post("/alertmanager")
def receive_alertmanager_webhook(payload: dict[str, Any]) -> dict:
    """Process firing and resolved notifications from Alertmanager."""
    alerts = payload.get("alerts", [])
    if not isinstance(alerts, list):
        raise HTTPException(status_code=400, detail="Invalid alerts payload")

    processed = []

    for item in alerts:
        labels = item.get("labels") or {}
        alert_name = labels.get("alertname", "UnknownAlert")
        scenario = labels.get("scenario", "unknown")
        service = labels.get("service", "unknown")
        status = item.get("status", payload.get("status", "firing"))

        if status not in {"firing", "resolved"}:
            continue

        incident = _find_active_incident(
            alert_name=alert_name,
            scenario=scenario,
            service=service,
        )

        if status == "firing":
            # Alertmanager may resend a firing notification.
            if incident is not None:
                processed.append({
                    "alert": alert_name,
                    "status": "already_exists",
                    "incident_id": incident.id,
                })
                continue

            severity = labels.get("severity", "SEV-2")
            if severity not in VALID_SEVERITIES:
                severity = "SEV-2"

            starts_at = item.get("startsAt")
            try:
                fired_at = (
                    datetime.fromisoformat(starts_at)
                    if starts_at
                    else datetime.now(UTC)
                )
                alert = Alert(
                    alert_name=alert_name,
                    severity=severity,
                    scenario=scenario,
                    service=service,
                    status="firing",
                    fired_at=fired_at,
                )
            except (ValueError, ValidationError) as exc:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid alert data: {exc}",
                ) from exc

            incident = incident_controller.create_incident(alert)
            incident_controller.run_rca(incident.id)

            processed.append({
                "alert": alert_name,
                "status": "incident_created",
                "incident_id": incident.id,
            })

        else:
            if incident is None:
                processed.append({
                    "alert": alert_name,
                    "status": "no_matching_active_incident",
                })
                continue

            for existing_alert in incident.alerts:
                if existing_alert.alert_name == alert_name:
                    existing_alert.status = "resolved"

            incident_controller.resolve_incident(incident.id)

            processed.append({
                "alert": alert_name,
                "status": "incident_resolved",
                "incident_id": incident.id,
            })

    return {
        "status": "success",
        "processed": processed,
    }

