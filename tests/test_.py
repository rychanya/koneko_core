from uuid import uuid4

import pytest
from koneko_core import Event, EventConflictError, EventNotExistError, MemoryEventStore, NewEventHasNextError

pytestmark = pytest.mark.anyio


@pytest.fixture
def empty_memory_event_store() -> MemoryEventStore:
    return MemoryEventStore()


@pytest.fixture
def event() -> Event:
    return Event(uid=uuid4(), previous_uid=None, next_uid=None)


class TestEmptyEventStore:
    async def test_get_last(self, empty_memory_event_store: MemoryEventStore) -> None:
        with pytest.raises(EventNotExistError):
            await empty_memory_event_store.get_last_event()

    async def test_add(self, empty_memory_event_store: MemoryEventStore, event: Event) -> None:
        await empty_memory_event_store.add(event)
        last_event = await empty_memory_event_store.get_last_event()
        assert last_event.uid == event.uid

    async def test_add_with_previus(self, empty_memory_event_store: MemoryEventStore, event: Event) -> None:
        event.previous_uid = uuid4()
        with pytest.raises(EventConflictError):
            await empty_memory_event_store.add(event)

    async def test_add_with_next(self, empty_memory_event_store: MemoryEventStore, event: Event) -> None:
        event.next_uid = uuid4()
        with pytest.raises(NewEventHasNextError):
            await empty_memory_event_store.add(event)
