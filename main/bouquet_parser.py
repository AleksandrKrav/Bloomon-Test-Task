import re
from collections import defaultdict
from typing import Optional

from .bouquet_design import BouquetDesign
from .flower import Flower


class BouquetParser:
    design_bouquet_pattern = re.compile(
        r'^(?P<bouquet_name>[A-Z]{1})(?P<bouquet_size>L|S)(?P<flowers>(\d+[a-z])+)(?P<quantity>\d+)$')
    design_bouquet_flower_pattern = re.compile(r'(\d+)(?P<flower_specie>[a-z])')

    flower_pattern = re.compile(
        r'^(?P<specie>[a-z])(?P<size>L|S)$'
    )

    @classmethod
    def parse_design_bouquet(cls, design_bouquet: str) -> Optional[BouquetDesign]:
        design_bouquet_group = re.match(cls.design_bouquet_pattern, design_bouquet)
        if not design_bouquet_group:
            return
        bouquet_size = design_bouquet_group['bouquet_size']
        bouquet_name = design_bouquet_group['bouquet_name']
        quantity = design_bouquet_group['quantity']

        parsed_flowers = re.findall(r'(\d+)([a-z])', design_bouquet_group['flowers'])
        flowers = defaultdict(int)
        for parsed_flower in parsed_flowers:
            flowers[parsed_flower[1]] = int(parsed_flower[0])
        return BouquetDesign(name=bouquet_name, size=bouquet_size, flowers=flowers, quantity=int(quantity))

    @classmethod
    def parse_flower(cls, flower: str) -> Optional[Flower]:
        flower_group = re.match(cls.flower_pattern, flower)
        if not flower_group:
            return
        return Flower(**flower_group.groupdict())
