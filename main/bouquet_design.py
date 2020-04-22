from dataclasses import dataclass
from typing import Dict

from .exceptions import SizeError


@dataclass
class BouquetDesign:
    name: str
    size: str
    flowers: Dict[str, int]
    quantity: int
    flowers_quantity: int = 0

    def __post_init__(self):
        if self.size not in ['S', 'L']:
            raise SizeError('Size could be one of: L or S')
        self.flowers_quantity = sum(self.flowers.values())

    def to_bouquet(self):
        sorted_flowers = {k[0]: self.flowers[k[0]] for k in sorted(self.flowers.items())}
        flowers = ''.join([f'{v}{k}' for k, v in sorted_flowers.items()])
        return f'{self.name}{self.size}{flowers}'
