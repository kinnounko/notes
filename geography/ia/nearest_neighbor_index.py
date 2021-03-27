import pandas as pd
import math
from scipy.spatial import KDTree
import numpy as np
from statistics import mean
import argparse


def box_select_coordinates(df, bndg_box):
    # Box select a certain region of geographical coordinates from a df
    x_bound = df[(bndg_box[0][0] < df['lat']) & (bndg_box[1][0] > df['lat'])]
    return x_bound[(bndg_box[0][1] < df['lon']) &
                   (bndg_box[1][1] > df['lon'])]


def box_area(bndg_box):
    dx = haversine_dist(bndg_box[0][0], bndg_box[0]
                        [1], bndg_box[1][0], bndg_box[0][1]) * 1000
    dy = haversine_dist(bndg_box[1][0], bndg_box[0]
                        [1], bndg_box[1][0], bndg_box[1][1]) * 1000

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
        # print(coords[0], coords[1], neighbor[0], neighbor[1])
    return mean(distances)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description='Calculate the Nearest Neighbor Index of a dataset')

    parser.add_argument('dataset', type=str,
                        help='absolute path to the dataset')

    parser.add_argument(
        '-b', '--bounding-box', help='choose an area bounded by 2 coordinates in comma-separated form: lat1,lon1,lat2,lon2', type=lambda s: [float(item) for item in s.split(',')])
    parser.add_argument(
        '-j', '--json', help='export bounded area to a json file')

    args = parser.parse_args()
    print(args.bounded)

    # DF must be in format lat, lon (comma separated)
    # TODO: argument parsed for dataset loc
    dataset = "/home/octo/velib.csv"
    df = pd.read_csv(dataset)

    # We get rid of any rows with non-numeric values
    df['lat'] = pd.to_numeric(df['lat'], errors='coerce')
    df['lon'] = pd.to_numeric(df['lon'], errors='coerce')
    df = df.dropna()

    # TODO: bounding box should be an argument (bottom left, top right)
    boundingbox = [[48.84881, 2.28708], [48.86075, 2.30742]]

    bounded = box_select_coordinates(df, boundingbox)

    #
    # We must put the coordinates in form [[lat, lon], [lat, lon]...]
    # there is probably a faster way to do this, this sucks
    #
    npbounded = []
    for i in range(len(bounded)):
        npbounded.append([bounded.iloc[i]['lat'], bounded.iloc[i]['lon']])

    npbounded = np.array(npbounded)

    #
    # We need to construct a k-n tree, as multiple queries will be made
    #

    print("Constructing k-d tree...")
    nni_querytree = KDTree(npbounded)

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

    print("Calculated NNI value for", args.dataset, nni_value(mean_observed_distance(
        npbounded, nni_querytree), box_area(boundingbox), len(npbounded)))


    if args.json is not None:
        # create JSON file
        json_file = bounded.to_json(orient='records')

        # export JSON file
        with open(args.json, 'w') as f:
            f.write(json_file)