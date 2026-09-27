from api.models import Alert, Incident
from controller.rca_engine import analyze_incident


def test_high_cpu_rca():
    alert = Alert(
        alert_name="HighCPU",
        severity="SEV-2",
        scenario="high-cpu",
        service="incident-simulator",
    )

    incident = Incident(
        id="INC-00001",
        title="High CPU detected",
        severity="SEV-2",
        status="INVESTIGATING",
        scenario="high-cpu",
        service="incident-simulator",
        alerts=[alert],
    )

    rca = analyze_incident(incident)

    assert rca.root_cause == (
        "CPU saturation caused by simulated CPU-intensive workload."
    )

    assert len(rca.evidence) >= 2
    assert rca.impact
    assert rca.recommendation
