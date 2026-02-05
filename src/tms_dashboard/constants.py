from enum import Enum
from dataclasses import dataclass, asdict
from typing import List

class TriggerType(Enum):
    DISABLED = 0
    STIMULUS = 1
    VIDEO = 2
    MUTE = 3
    PARALLEL = 4

@dataclass
class BrainTargetModel:
    position: List[float] = (0, 0, 0)
    orientation: List[float] = (0, 0, 0)
    color: List[float] = (0, 0, 1)
    length: float = 0
    mtms: List[float] = (0, 0, 0, 0)
    mep: float = 0

    def to_dict(self) -> dict:
        return asdict(self)