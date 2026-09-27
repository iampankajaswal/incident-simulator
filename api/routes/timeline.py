from fastapi import APIRouter, HTTPException

from api.models import TimelineEvent
from api.routes.scenarios import incident_controller

router = APIRouter(
    prefix="/incidents",
    tags=["timeline"],
)


@router.get(
    "/{incident_id}/timeline",
    response_model=list[TimelineEvent],
)
def get_timeline(incident_id: str) -> list[TimelineEvent]:
    try:
        incident = incident_controller.get_incident(incident_id)
    except KeyError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc

    return incident.timeline
