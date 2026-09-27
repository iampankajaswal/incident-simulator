#from datetime import datetime, timezone
from datetime import UTC, datetime
from typing import Literal

from pydantic import BaseModel, Field


def utc_now() -> datetime:
    #return datetime.now(timezone.utc)
     return datetime.now(UTC)


IncidentStatus = Literal[
    "OPEN",
    "INVESTIGATING",
    "MITIGATED",
    "RESOLVED",
]

Severity = Literal[
    "SEV-1",
    "SEV-2",
    "SEV-3",
    "SEV-4",
]


class Alert(BaseModel):
    alert_name: str
    severity: Severity
    scenario: str
    service: str
    status: Literal["firing", "resolved"] = "firing"
    fired_at: datetime = Field(default_factory=utc_now)


class TimelineEvent(BaseModel):
    timestamp: datetime = Field(default_factory=utc_now)
    event_type: str
    message: str


class RCAResult(BaseModel):
    root_cause: str
    evidence: list[str]
    impact: str
    recommendation: str


class Incident(BaseModel):
    id: str
    title: str
    severity: Severity
    status: IncidentStatus
    scenario: str
    service: str
    created_at: datetime = Field(default_factory=utc_now)
    resolved_at: datetime | None = None
    alerts: list[Alert] = Field(default_factory=list)
    timeline: list[TimelineEvent] = Field(default_factory=list)
    rca: RCAResult | None = None


class ScenarioRunRequest(BaseModel):
    duration: int = Field(default=5, ge=1, le=60)
    workers: int = Field(default=1, ge=1, le=4)


class ScenarioRunResponse(BaseModel):
    scenario: str
    status: str
    incident_id: str
    message: str


class IncidentListResponse(BaseModel):
    incidents: list[Incident]
