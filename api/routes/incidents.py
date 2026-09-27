from fastapi import APIRouter, HTTPException

from api.models import Incident
from api.routes.scenarios import incident_controller

router = APIRouter(
    prefix="/incidents",
    tags=["incidents"],
)


@router.get("", response_model=list[Incident])
def list_incidents() -> list[Incident]:
    return incident_controller.list_incidents()


@router.get("/{incident_id}", response_model=Incident)
def get_incident(incident_id: str) -> Incident:
    try:
        return incident_controller.get_incident(incident_id)
    except KeyError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc


@router.post("/{incident_id}/resolve", response_model=Incident)
def resolve_incident(incident_id: str) -> Incident:
    try:
        return incident_controller.resolve_incident(incident_id)
    except KeyError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc
