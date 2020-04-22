import functools
import operator
from collections import defaultdict, Counter
from typing import List, Dict

from .bouquet_design import BouquetDesign
from .flower import Flower


class Florist:

    def __init__(self):
        self._flowers = []
        self._bouquet_designs: List[BouquetDesign] = []
        self._small_flowers: dict = defaultdict(int)
        self._large_flowers: dict = defaultdict(int)

    def add_flower(self, flower: Flower):
        if flower.size == 'L':
            self._large_flowers[flower.specie] += 1
        else:
            self._small_flowers[flower.specie] += 1

    def add_bouquet_design(self, bouquet_design: BouquetDesign):
        self._bouquet_designs.append(bouquet_design)

    def make_bouquets(self) -> List[str]:
        """
        Steps of algorithm:
        1) sort large and small flowers by max quantities
        2) if bouquet not needed in extra flowers, skip thi step
        3) get needed flowers for a bouquet
        4) merge received flowers with existing flowers in design bouquet
        5) put ready bouquet to result array

        Return: list of bouquets

        """
        self._sort_flowers()  # 1

        result = []
        for design_bouquet in self._bouquet_designs:
            needed_flowers = design_bouquet.quantity - design_bouquet.flowers_quantity  # 2

            if needed_flowers == 0:  # 2
                result.append(design_bouquet.to_bouquet())
                continue

            extra_flowers = self._get_lacking_flowers(design_bouquet.size, needed_flowers)  # 3

            if extra_flowers:
                updated_flowers = dict(
                    functools.reduce(
                        operator.add,
                        map(Counter, [design_bouquet.flowers, extra_flowers])
                    ))  # 4
                design_bouquet.flowers = updated_flowers
            result.append(design_bouquet.to_bouquet())  # 5

        return result

    def _sort_flowers(self, size: str = None):
        if size == 'L' or not size:
            self._large_flowers = {k[0]: self._large_flowers[k[0]] for k in sorted(self._small_flowers.items())}
        if size == 'S' or not size:
            self._small_flowers = {k[0]: self._small_flowers[k[0]] for k in sorted(self._small_flowers.items())}

    def _get_lacking_flowers(self, size: str, quantity: int) -> Dict[str, int]:
        """
        Steps of algorithm:
        1) try get max flower quantities from every items in existing flowers according to size
        2) if flower quantities does not enough try to get max flower quantities in next element from dict
        until flowers are finished or needed quantities of getting flowers will be enough

        Return: dict of extra flowers for bouquets
        """
        flowers = self._small_flowers if size == 'S' else self._large_flowers
        result = defaultdict(int)
        for specie, flower_quantity in flowers.items():
            remaining_flowers = quantity - flower_quantity

            if remaining_flowers < 0:
                """
                Get needed quantity of flowers and break the for
                """
                flowers[specie] = abs(remaining_flowers)
                result[specie] = quantity
                break

            quantity = abs(remaining_flowers)
            result[specie] = flower_quantity
            flowers[specie] = 0

        # sorting flowers for the next step. for getting max quantities flowers at the beginning
        self._sort_flowers(size)
        return result
