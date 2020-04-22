from dataclasses import dataclass

from .exceptions import SizeError


@dataclass
class Flower:
    specie: str
    size: str

    def __post_init__(self):
        if self.size not in ['S', 'L']:
            raise SizeError('Size could be one of: L or S')
