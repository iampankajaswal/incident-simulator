from fastapi import FastAPI

from api.routes import incidents, scenarios, timeline

app = FastAPI(
    title="Incident Management Simulator",
    description=(
        "Simulate infrastructure incidents and automatically "
        "generate alerts, incidents, timelines and RCA."
    ),
    version="0.1.0",
)


@app.get("/health", tags=["system"])
def health() -> dict:
    return {
        "status": "healthy",
        "service": "incident-simulator",
    }


app.include_router(scenarios.router)
app.include_router(incidents.router)
app.include_router(timeline.router)
