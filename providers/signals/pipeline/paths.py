from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class PipelinePaths:
    radar_root: Path
    date: str  # YYYY-MM-DD

    @property
    def dir(self) -> Path:
        return self.radar_root / "_pipeline" / self.date

    @property
    def signals(self) -> Path:
        return self.dir / "signals.jsonl"

    @property
    def enriched(self) -> Path:
        return self.dir / "enriched.jsonl"

    @property
    def clusters(self) -> Path:
        return self.dir / "clusters.json"

    @property
    def run_meta(self) -> Path:
        return self.dir / "run_meta.json"

    @property
    def legacy_raw(self) -> Path:
        return self.radar_root / "_raw" / f"{self.date}.jsonl"

    def ensure(self) -> None:
        self.dir.mkdir(parents=True, exist_ok=True)
        self.legacy_raw.parent.mkdir(parents=True, exist_ok=True)
