
from fastapi import FastAPI

from api.metrics import metrics_response
from api.routes import incidents, scenarios, timeline, webhooks

app = FastAPI(
    title="Incident Management Simulator",
    description=(
        "Simulate infrastructure incidents and automatically "
        "generate alerts, incidents, timelines and RCA."
    ),
    version="0.2.0",
)


@app.get("/health", tags=["system"])
def health() -> dict:
    return {
        "status": "healthy",
        "service": "incident-simulator",
    }


@app.get("/metrics", include_in_schema=False)
def metrics():
    return metrics_response()


app.include_router(scenarios.router)
app.include_router(incidents.router)
app.include_router(timeline.router)
app.include_router(webhooks.router)
