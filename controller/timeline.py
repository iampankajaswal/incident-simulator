from api.models import Incident, TimelineEvent


def add_event(
    incident: Incident,
    event_type: str,
    message: str,
) -> TimelineEvent:
    event = TimelineEvent(
        event_type=event_type,
        message=message,
    )

    incident.timeline.append(event)

    return event
