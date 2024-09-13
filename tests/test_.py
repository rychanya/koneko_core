import pytest
from koneko_core import EventStore

pytestmark = pytest.mark.anyio


async def test_event_store() -> None:
    store = EventStore()
    store.events = list(range(7))
    assert await store.get_last_events(2) == [2, 3, 4, 5, 6]
