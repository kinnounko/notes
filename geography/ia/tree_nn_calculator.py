import pandas as pd
import math
from scipy.spatial import KDTree
import numpy as np
from statistics import mean


treedataset = "/home/octo/les-arbres.csv"
df = pd.read_csv(treedataset)

# Show dataframe
df1 = df[df['arr'] == 'PARIS 16E ARRDT']
df2 = df[df['arr'] == 'PARIS 7E ARRDT']
df = pd.merge(df1, df2, how='outer')


def box_select_coordinates(df, x1, y1, x2, y2):
    # Box select a certain region of geographical coordinates from a df

    x_bound = df[(x1 < df['lat']) & (x2 > df['lat'])]
    result = x_bound[(y1 < df['lon']) & (y2 > df['lon'])]

    return result


def box_area(x1, y1, x2, y2):
    dx = haversine_dist(x1, y1, x2, y1) * 1000
    dy = haversine_dist(x2, y1, x2, y2) * 1000

    return dx*dy


def haversine_dist(lat1, lon1, lat2, lon2):
    # Haversine distance between two coordinates

    dlat = (math.pi / 180) * (lat2 - lat1)
    dlon = (math.pi / 180) * (lon2 - lon1)

    lat1 = (math.pi / 180) * (lat1)
    lat2 = (math.pi / 180) * (lat2)

    a = math.pow(math.sin(dlat / 2), 2) + \
        math.pow(math.sin(dlon / 2), 2) * math.cos(lat1) * math.cos(lat2)
    rad = 6371
    c = 2 * math.asin(math.sqrt(a))
    return rad * c


def nni_value(dobs, a, n):
    # Calculate NNI value:
    #  I------------I----------I
    #  0.00         1.0       2.15
    #  clustered   random   regular
    return dobs / (0.5 * math.sqrt(a / n))


def mean_observed_distance(coordsarr, kdtree):
    distances = []
    for coords in coordsarr:
        d, i = kdtree.query((coords[0], coords[1]), workers=-1, k=[2])
        neighbor = coordsarr[i]
        distances.append(haversine_dist(
            coords[0], coords[1], neighbor[0][0], neighbor[0][1]) * 1000)
        #print(coords[0], coords[1], neighbor[0], neighbor[1])
    return mean(distances)


df['lat'] = pd.to_numeric(df['lat'], errors='coerce')
df = df.dropna()

sixtbbox = [[48.85373, 2.26728], [48.86042, 2.27865]]
sevtbbox = [[48.84881, 2.28708], [48.86075, 2.30742]]

sixteenth = box_select_coordinates(
    df, sixtbbox[0][0], sixtbbox[0][1], sixtbbox[1][0], sixtbbox[1][1])
seventh = box_select_coordinates(
    df, sevtbbox[0][0], sevtbbox[0][1], sevtbbox[1][0], sevtbbox[1][1])

#
# We must put the coordinates in form [[lat, lon], [lat, lon]...]
# there is probably a faster way to do this, this sucks
#
seventharr = []
sixteentharr = []
for i in range(len(seventh)):
    seventharr.append([seventh.iloc[i]['lat'], seventh.iloc[i]['lon']])
for i in range(len(sixteenth)):
    sixteentharr.append([sixteenth.iloc[i]['lat'], sixteenth.iloc[i]['lon']])

seventharr = np.array(seventharr)
sixteentharr = np.array(sixteentharr)

#
# We need to construct a k-n tree, as multiple queries will be made
#

print("Constructing k-d tree...")
sixteenth_kdtree = KDTree(sixteentharr)

print("Constructing k-d tree...")
seventh_kdtree = KDTree(seventharr)

#
# POC: this works, the point returned is the closest.
# d, i = sixteenth_kdtree.query((48.85591, 2.27495), workers=-1)
# print("closest point:", sixteentharr[i])
#

#
# We must then calculate the NNI:
#
# Rn = D(Obs)/         where: a is the area observed, n is the number of points, D(Obs) is the mean observed distance to the nearest neighbor
#   0.5(sqrt(a/n))
#
# Loop through all coordinates, finding their nearest neighbor and calculating the distance using the haversine formula
#


print("Seventh arr. NNI value: ", nni_value(mean_observed_distance(seventharr, seventh_kdtree), box_area(
    sevtbbox[0][0], sevtbbox[0][1], sevtbbox[1][0], sevtbbox[1][1]), len(seventharr)))

print("Sixteenth arr. NNI value: ", nni_value(mean_observed_distance(sixteentharr, sixteenth_kdtree), box_area(
    sixtbbox[0][0], sixtbbox[0][1], sixtbbox[1][0], sixtbbox[1][1]), len(sixteentharr)))

#
# For map info, can be parsed with the leaflet map
#
'''
out = pd.merge(sixteenth, seventh, how='outer')

# create JSON file
json_file = out.to_json(orient='records')

# export JSON file
with open('trees.json', 'w') as f:
    f.write(json_file)
'''
