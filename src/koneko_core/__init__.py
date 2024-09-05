class EventStore[Event]:
    events: list[Event]

    async def add(self, event: Event) -> None:
        self.events.append(event)

    async def get_last_events(self, count: int, last_event_id: int) -> list[Event]:
        return self.events[last_event_id : last_event_id + count]
