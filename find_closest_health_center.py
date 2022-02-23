import pandas as pd
import numpy as np
from geopy import distance


centroid_locs = pd.read_csv('mphia2015centroids.csv').set_index('centroidid')
health_center_locs = pd.read_excel('00 SSA MFL (130219).xlsx').set_index('Country').loc['Malawi',:].reset_index().dropna()


for i, centroid in enumerate(centroid_locs.index):
    if (i % 50) == 0:
        print(i)
    centroid_lat = centroid_locs.at[centroid,'latitude']
    centroid_lon = centroid_locs.at[centroid,'longitude']
    centroid_coordinates = [centroid_lat, centroid_lon]
    min_distance = np.inf
    closest_index = health_center_locs.index[0]
    for health_center_id in health_center_locs.index:
        health_center_lat = health_center_locs.at[health_center_id, 'Lat']
        health_center_lon = health_center_locs.at[health_center_id, 'Long']
        health_center_coordinates = [health_center_lat, health_center_lon]
        distance_from_center = distance.distance(centroid_coordinates, health_center_coordinates).km
        if distance_from_center < min_distance:
            min_distance = distance_from_center
            closest_index = health_center_id
    centroid_locs.loc[centroid,'distance'] = min_distance
    centroid_locs.loc[centroid,'Facility type'] = health_center_locs.at[closest_index,'Facility type']
    centroid_locs.loc[centroid,'Ownership'] = health_center_locs.at[closest_index,'Ownership']

centroid_locs.to_csv('centroids_with_heath_center.csv')