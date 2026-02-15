import dataclasses
from typing import Optional, List


@dataclasses.dataclass
class Data:
    n: Optional[int]
    matrix: Optional[List[List[float]]]
    accuracy: Optional[float]


@dataclasses.dataclass
class Result:
    x: List[float]
    iterations: int
    errors: List[float]
    norm: float
