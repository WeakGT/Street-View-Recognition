import shapefile
from shapely.geometry import Point, shape
import numpy as np
from collections import Counter

shp = shapefile.Reader('shapefiles/TM_WORLD_BORDERS-0.3.shp', encoding='latin1') 
# 不要用notepad開，會crash:( 查查看有沒有轉成UTF-8的辦法
# 找城市單位的shapefile...? 

EU3 = ['ARM', 'BIH', 'BIH', 'CYP', 'DNK', 'IRL', 'AUT', 'EST', 'CZE', 'FIN', 
       'FRA', 'DEU', 'GRC', 'HRV', 'HUN', 'ISL', 'ITA', 'LTU', 'LVA', 'BLR', 
       'MLT', 'BEL', 'AND', 'GIB', 'LUX', 'MCO', 'NLD', 'NOR', 'POL', 'PRT', 
       'ROU', 'MDA', 'ESP', 'CHE', 'GBR', 'SRB', 'SWE', 'ALB', 'MKD', 'MNE', 
       'SVK', 'SVN']  # 'TUR'

EU = [(boundary, record) for boundary, record in 
      zip(shp.shapes(), shp.records()) if record[2] in EU3]

count = Counter()

def sample(shapes, min_x=-11, max_x=26, min_y=37, max_y=71):
    while True:
        point = (np.random.uniform(min_x, max_x), np.random.uniform(min_y, max_y)) 
        for boundary, record in sorted(shapes, key=lambda x: -count[x[1][2]]):
            if Point(point).within(shape(boundary)): 
                count[record[2]] += 1
                return point

def generate_coordinates(shapes, num_points=100, min_x=-11, max_x=26, min_y=37, max_y=71):
    coordinates = []
    for _ in range(num_points):
        point = sample(shapes, min_x, max_x, min_y, max_y)
        coordinates.append(point)
    return coordinates