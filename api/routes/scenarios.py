from fastapi import APIRouter, HTTPException

from api.models import Alert, ScenarioRunRequest, ScenarioRunResponse
from controller.incident_controller import IncidentController
from simulator.cpu.stress import run_cpu_stress

router = APIRouter(
    prefix="/scenarios",
    tags=["scenarios"],
)

incident_controller = IncidentController()


@router.get("")
def list_scenarios() -> dict:
    return {
        "scenarios": [
            {
                "name": "high-cpu",
                "description": "Simulate CPU saturation.",
                "status": "available",
            }
        ]
    }


@router.post(
    "/high-cpu/run",
    response_model=ScenarioRunResponse,
)
def run_high_cpu(request: ScenarioRunRequest) -> ScenarioRunResponse:
    try:
        run_cpu_stress(
            duration=request.duration,
            workers=request.workers,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    alert = Alert(
        alert_name="HighCPU",
        severity="SEV-2",
        scenario="high-cpu",
        service="incident-simulator",
    )

    incident = incident_controller.create_incident(alert)

    incident_controller.run_rca(incident.id)
    incident_controller.resolve_incident(incident.id)

    return ScenarioRunResponse(
        scenario="high-cpu",
        status="completed",
        incident_id=incident.id,
        message=(
            f"High CPU simulation completed and incident "
            f"{incident.id} was generated."
        ),
    )
