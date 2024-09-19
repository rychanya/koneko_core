import abc
from dataclasses import dataclass
from uuid import UUID


class BaseEventStoreError(Exception):
    ...


class MissingParentError(BaseEventStoreError):
    ...


class ParentNotFoundError(BaseEventStoreError):
    ...


class EventNotLastError(BaseEventStoreError):
    ...


class EventNotExistError(BaseEventStoreError):
    ...


class NewEventHasNextError(BaseEventStoreError):
    ...


class EventConflictError(BaseEventStoreError):
    ...


@dataclass
class Event:
    uid: UUID
    previous_uid: UUID | None
    next_uid: UUID | None


class AbstractEventStore(abc.ABC):  # pragma: no cover
    @abc.abstractmethod
    async def add(self, event: Event) -> None:
        ...

    @abc.abstractmethod
    async def get_event_by_id(self, event_id: UUID) -> Event:
        ...

    @abc.abstractmethod
    async def get_last_event(self) -> Event:
        ...


class MemoryEventStore(AbstractEventStore):
    def __init__(self) -> None:
        self._events: dict[UUID, Event] = dict()
        self._last_event_id: UUID | None = None

    async def add(self, event: Event) -> None:
        if event.next_uid is not None:
            raise NewEventHasNextError
        if event.previous_uid is None:
            if self._last_event_id is None:
                self._events[event.uid] = event
                self._last_event_id = event.uid
                return
            else:
                raise EventConflictError
        try:
            last_event = await self.get_last_event()
        except EventNotExistError as error:
            raise EventConflictError from error
        if event.previous_uid != last_event.uid:
            raise EventNotLastError
        self._events[event.uid] = event
        last_event.next_uid = event.uid
        self._last_event_id = event.uid

    async def get_event_by_id(self, event_id: UUID) -> Event:
        try:
            return self._events[event_id]
        except KeyError as error:
            raise EventNotExistError from error

    async def get_last_event(self) -> Event:
        if self._last_event_id is None:
            raise EventNotExistError
        return await self.get_event_by_id(event_id=self._last_event_id)
