from __future__ import annotations

from dataclasses import dataclass, field
from threading import Lock


@dataclass
class MetricsStore:
    request_total: int = 0
    request_errors_total: int = 0
    request_by_path: dict[str, int] = field(default_factory=dict)
    request_by_status_class: dict[str, int] = field(default_factory=dict)
    _lock: Lock = field(default_factory=Lock, repr=False)

    def record(self, path: str, status_code: int) -> None:
        status_class = f"{status_code // 100}xx"
        with self._lock:
            self.request_total += 1
            if status_code >= 400:
                self.request_errors_total += 1
            self.request_by_path[path] = self.request_by_path.get(path, 0) + 1
            self.request_by_status_class[status_class] = (
                self.request_by_status_class.get(status_class, 0) + 1
            )

    def snapshot(self) -> dict:
        with self._lock:
            return {
                "request_total": self.request_total,
                "request_errors_total": self.request_errors_total,
                "request_by_path": dict(self.request_by_path),
                "request_by_status_class": dict(self.request_by_status_class),
            }
