import numpy as np
from stravalib import Client
from typing import Optional, List, Tuple, NamedTuple, Iterable
from functools import partial
from shapely.geometry import LineString
from sklearn.neighbors import BallTree

import itertools
from wandrer.utils import round_coordinates, sample_coords_by_distance, calculate_midpoint, segment_intersection, segment_length, complementary_region
from wandrer.client import StravaClient

class HistoricalActivities():
    def __init__(self, strava_client: StravaClient, types: Optional[List[str]] = None, limit: int = 10):
        self.strava_client = strava_client
        self.types = types or ['latlng', 'distance']
        self.limit = limit
        self.path_segments = []
        self.strava_segments = []
        self.midpoints = []
        self.tree_index = False

    def fetch_path_segments(self, sampling_interval: int = 500) -> Tuple[np.ndarray, np.ndarray]:
        activities = list(itertools.islice(self.strava_client.get_activities(), self.limit))
        existing_segments = set()
        for activity in activities:
            activity = Activity(strava_client=self.strava_client, activity_id=activity.id, types=self.types)
            activity.fetch_path_segments(sampling_interval=sampling_interval)
    
            for segment in activity.path_segments:
                segment_key = tuple(sorted(segment))
                if segment_key not in existing_segments:
                    self.path_segments.append(tuple(segment))
                    existing_segments.add(segment_key)
                    midpoint = calculate_midpoint(segment)
                    self.midpoints.append(midpoint)

        self.path_segments_np = np.array(self.path_segments)
        self.midpoints_np= np.array([(mp[0], mp[1]) for mp in self.midpoints])

    def fetch_strava_segments(self):
        activities = list(itertools.islice(self.strava_client.get_activities(), self.limit))
        existing_segments = set()
        for activity in activities:
            activity = Activity(strava_client=self.strava_client, activity_id=activity.id, types=self.types)
            activity.fetch_strava_segments()

            for segment in activity.strava_segments:
                segment_key = tuple(sorted(segment))
                if segment_key not in existing_segments:
                    self.strava_segments.append(tuple(segment))
                    existing_segments.add(segment_key)
    
    def index(self) -> BallTree:
        midpoints = np.array([[np.deg2rad(lat), np.deg2rad(lon)] for lat, lon in self.midpoints_np])
        self.tree_index = BallTree(midpoints, metric='haversine')
        return self.tree_index

class Activity:
    def __init__(self, strava_client: StravaClient, activity_id, types: Optional[List[str]] = None):
        self.strava_client = strava_client
        self.activity_id = activity_id
        self.types = types or ['latlng', 'distance']
        self.path_segments = []
        self.strava_segments = []

    def fetch_strava_segments(self):
        activity_segments = self.strava_client.client.get_activity(self.activity_id, include_all_efforts="True").segment_efforts
        for seg in activity_segments:
            name = seg.name
            start_latlng = seg.to_dict()['segment']['end_latlng']
            end_latlng = seg.to_dict()['segment']['start_latlng']
            self.strava_segments.append({"name": name, "start_latlng": start_latlng, "end_latlng": end_latlng})

    def fetch_path_segments(self, sampling_interval=500):
        activity_data = self.strava_client.client.get_activity_streams(self.activity_id, types=self.types)
        if 'latlng' in activity_data.keys():
            coords=round_coordinates(activity_data['latlng'].data[:])
            dists = (activity_data['distance'].data[:])

            sampled_coords = sample_coords_by_distance(coords, dists, sampling_interval=sampling_interval)

            self.path_segments = [(tuple(sampled_coords[i]), tuple(sampled_coords[i+1])) for i in range(len(sampled_coords)-1)]
            self.midpoints = np.array([calculate_midpoint(segment) for segment in self.path_segments])
        else:
            print("No lat long data for this activity")

    def get_new_path_segments(self, history: HistoricalActivities):
        if self.path_segments == []:
            self.fetch_path_segments()

        if not history.tree_index:
            history.index()

        tree = history.tree_index
        sampling_interval = 500
        search_radius = sampling_interval / 6371e3

        shared_segments = []
        remainder_segments = []
        test_list = np.array([[np.deg2rad(lat), np.deg2rad(lon)] for lat, lon in self.midpoints])

        for idx, test_point in enumerate(test_list):
            ind = tree.query_radius(test_point.reshape(1, -1), r=search_radius)
            if ind[0].size>0:
                full_intersect = []
                for point in ind[0]:
                    seg = history.path_segments_np[point]
                    inter = segment_intersection(seg, self.path_segments[idx])
                    inter_size = segment_length(inter)
                    if inter_size > 0:
                        shared_segments.append(inter)
                        full_intersect.append(inter)
                if len(full_intersect) > 0:
                    remainder_seg = complementary_region(full_intersect, self.path_segments[idx])
                    if len(remainder_seg) > 0:
                        remainder_segments.append(remainder_seg)
            else:
                remainder_segments.append(self.path_segments[idx])

        self.new_path_segments=remainder_segments
        self.shared_path_segments=shared_segments 

        return self.new_path_segments

    def get_new_strava_segments(self, history: HistoricalActivities):
        if self.strava_segments == []:
            self.fetch_strava_segments()
        if history.strava_segments == []:
            history.fetch_strava_segments()
        if not history.tree_index:
            history.index()
        #TODO: do filtering with nearest neighbour search on midpointss
        new_strava_segments = [seg for seg in self.strava_segments if seg not in history.strava_segments]
        return new_strava_segments
