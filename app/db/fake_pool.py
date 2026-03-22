import threading
from dataclasses import dataclass


@dataclass
class FakeConnection:
    conn_id: int

    def execute(self, statement: str) -> None:
        _ = statement


class FakePool:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._next_id = 0
        self._active = 0

    def acquire(self) -> FakeConnection:
        with self._lock:
            self._next_id += 1
            self._active += 1
            return FakeConnection(conn_id=self._next_id)

    def release(self, conn: FakeConnection) -> None:
        _ = conn
        with self._lock:
            if self._active > 0:
                self._active -= 1

    def active_connections(self) -> int:
        with self._lock:
            return self._active
