import numpy as np
import shapely.geometry as geometry
from shapely import intersection
from geopy.distance import geodesic

def round_coordinates(coords, precision=3):
    """Rounds a list of GPS coordinates."""
    return [[round(x, ndigits=precision), round(y, ndigits=precision)] for x, y in coords]

def sample_coords_by_distance(coords, dists, sampling_interval=500):
    """Sample GPS coordinates based on cumulative distances.

    Args:
      coords: List of GPS coordinates in the form of (lat, lon) tuples.
      dists: List of cumulative distances in meters corresponding to each GPS coordinate.
      sampling_interval: Distance threshold in meters for selecting GPS coordinates.

    Returns:
      Sampled GPS coordinates in the form of a list of (lat, lon) tuples.
    """
    distances = np.array(dists)
    current_distance = 0
    indices = []
    for i, dist in enumerate(distances):
        if dist > current_distance + sampling_interval:
            indices.append(i)
            current_distance = dist
    indices.append(len(distances)-1)
    sampled_coords = [coords[idx] for idx in indices]
    #compression_ratio = len(coords) / len(sampled_coords)
    return sampled_coords

def calculate_midpoint(segment):
    """Calculates the midpoint between two GPS coordinate tuples."""
    coord1 = segment[0]
    coord2 = segment[1]

    lat_mid = round((coord1[0] + coord2[0]) / 2., ndigits=3)
    lon_mid = round((coord1[1] + coord2[1]) / 2., ndigits=3)
    midpoint = (lat_mid, lon_mid)

    return midpoint

def segment_intersection(segment1, segment2):
    line1 = geometry.LineString(segment1)
    line2 = geometry.LineString(segment2)
    inter = list(intersection(line1, line2).coords)
    return inter

def segment_length(segment):
    if len(segment)>1:
        return geodesic(segment[0], segment[1]).kilometers
    else:
        return 0

def complementary_region(S1,  S2):
    """Compute the complementary region of S1 in S2 using Shapely."""

    united_lines = geometry.LineString(sum([list(x) for x in S1], []))
    diff = geometry.LineString(S2).difference(united_lines)

    if isinstance(diff, list):
        return [list(geom.coords[0]) for geom in diff]
    elif isinstance(diff, geometry.base.BaseGeometry):
        if diff.is_empty:
            return []
        else:
            return [list(diff.coords[0])]
    else:
        raise NotImplementedError("Unexpected type found during difference operation.")