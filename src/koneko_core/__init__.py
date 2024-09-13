from uuid import UUID


class MissingParentError(Exception):
    ...


class ParentNotFoundError(Exception):
    ...


class EventNotLastError(Exception):
    ...


class Event:
    uid: UUID
    previous_uid: UUID | None
    next_uid: UUID | None


class EventStore:
    last_event_uid: UUID
    events: dict[UUID, Event]

    async def add(self, event: Event) -> None:
        if event.previous_uid is None:
            if self.events:
                raise MissingParentError
            else:
                self.events[event.uid] = event
                return

        previous_event = self.events.get(event.previous_uid)
        if previous_event is None:
            raise ParentNotFoundError
        if previous_event.next_uid is not None:
            raise EventNotLastError
        self.events[event.uid] = event
        previous_event.next_uid = event.uid
