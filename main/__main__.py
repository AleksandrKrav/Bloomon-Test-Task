import os

from .bouquet_parser import BouquetParser
from .florist import Florist

if __name__ == '__main__':

    path = os.path.join(os.path.dirname(__file__), '../sample.txt')
    parser = BouquetParser
    florist = Florist()

    with open(path) as file:
        flower_specie_flag = False
        line = file.readline()
        while line:
            line = line.replace('\n', '')
            if not line:
                flower_specie_flag = True
                line = file.readline()
                continue
            try:
                if flower_specie_flag:
                    flower = parser.parse_flower(line)
                    if flower:
                        florist.add_flower(flower)
                else:
                    design_bouquet = parser.parse_design_bouquet(line)
                    if design_bouquet:
                        florist.add_bouquet_design(design_bouquet)
            except Exception as e:
                print(f'Failed parse error line: {e}')
            line = file.readline()

    bouquets = florist.make_bouquets()
    for bouquet in bouquets:
        print(bouquet)
