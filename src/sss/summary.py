from dataclasses import dataclass
from pathlib import Path

@dataclass(slots=True, kw_only=True)
class Summary:
    """Aggregiert Move-/Dry-Run-Zahlen für einen Durchlauf."""
    out_root: Path
    moved: int = 0
    simulated: int = 0

    def inc_moved(self, n: int = 1) -> None:
        """Erhöhe 'moved' um n (n >= 0)."""
        if n < 0:
            raise ValueError("n must be >= 0")
        self.moved += n

    def inc_simulated(self, n: int = 1) -> None:
        """Erhöhe 'simulated' um n (n >= 0)."""
        if n < 0:
            raise ValueError("n must be >= 0")
        self.simulated += n

    @property
    def total(self) -> int:
        """Summe aus real verschoben + nur simuliert."""
        return self.moved + self.simulated

    def render(self) -> str:
        return (
            f"Zusammenfassung: gesamt={self.total} | "
            f"verschoben={self.moved} | simuliert={self.simulated} | "
            f"zielbasis={self.out_root}"
        )

    def __str__(self) -> str:  
        return self.render()
