from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class SalesPipelinePaths:
    sales_root: Path
    date: str  # YYYY-MM-DD

    @property
    def dir(self) -> Path:
        return self.sales_root / "_pipeline" / self.date

    @property
    def signals(self) -> Path:
        return self.dir / "signals.jsonl"

    @property
    def qualified(self) -> Path:
        return self.dir / "qualified.jsonl"

    @property
    def beachheads(self) -> Path:
        return self.dir / "beachheads.json"

    @property
    def run_meta(self) -> Path:
        return self.dir / "run_meta.json"

    @property
    def verdict(self) -> Path:
        return self.dir / "verdict.md"

    @property
    def inbox_x_manual(self) -> Path:
        return self.sales_root / "inbox" / "x-manual.jsonl"

    def ensure(self) -> None:
        self.dir.mkdir(parents=True, exist_ok=True)
        self.inbox_x_manual.parent.mkdir(parents=True, exist_ok=True)
