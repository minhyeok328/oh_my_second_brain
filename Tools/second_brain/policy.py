from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path, PurePosixPath


@dataclass(frozen=True)
class Route:
    action: str
    target: str
    metadata: dict[str, object]


@dataclass(frozen=True)
class MigrationPolicy:
    archive_root: str
    status_routes: dict[str, dict[str, object]]
    path_routes: dict[str, dict[str, object]]
    archive_fallback: bool = True

    @classmethod
    def load(cls, path: Path) -> "MigrationPolicy":
        data = json.loads(path.read_text(encoding="utf-8"))
        return cls(data["archive_root"], data["status_routes"], data["path_routes"], data.get("archive_fallback", True))

    def route(self, path: str, status: str) -> Route:
        normalized = PurePosixPath(path).as_posix()
        config = self.path_routes.get(normalized) or self.status_routes.get(status)
        if config is None:
            if not self.archive_fallback:
                raise ValueError(f"no route for {normalized}")
            return Route("archive", f"{self.archive_root}/{normalized}", {})
        filename = PurePosixPath(normalized).name
        prefix = str(config.get("strip_prefix", ""))
        if prefix and filename.startswith(prefix):
            filename = filename[len(prefix):]
        suffix = str(config.get("append_suffix", ""))
        if suffix:
            stem, extension = filename.rsplit(".", 1)
            filename = f"{stem}{suffix}.{extension}"
        target = str(PurePosixPath(str(config["target"])) / filename) if str(config["target"]).endswith("/") else str(config["target"])
        # Explicit routes already provide a complete file target; status routes provide a directory.
        if normalized not in self.path_routes:
            target = str(PurePosixPath(str(config["target"])) / filename)
        metadata = {key: value for key, value in config.items() if key not in {"target", "strip_prefix", "append_suffix"}}
        return Route("move", target, metadata)
