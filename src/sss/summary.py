
from dataclasses import dataclass
from pathlib import Path

@dataclass
class Summary:
    out_root: Path
    moved: int = 0
    simulated: int = 0

    def inc_moved(self) -> None:
        self.moved += 1

    def inc_simulated(self) -> None:
        self.simulated += 1

    @property
    def total(self) -> int:
        return self.moved + self.simulated

    def render(self) -> str:
        return (
            f"Zusammenfassung: gesamt={self.total} | "
            f"verschoben={self.moved} | simuliert={self.simulated} | "
            f"zielbasis={self.out_root}"
        )
