import os
from dataclasses import dataclass
from typing import List
from dotenv import load_dotenv
from stravalib.client import Client

load_dotenv()

@dataclass
class StravaClient:
    access_token: str = os.environ["STRAVA_ACCESS_TOKEN"]
    refresh_token: str = os.environ["STRAVA_REFRESH_TOKEN"]
    client_id: str = os.environ["STRAVA_CLIENT_ID"]
    client_secret: str = os.environ["STRAVA_CLIENT_SECRET"]

    client = Client()

    def configure_client(self):
        self.client.access_token = self.access_token
        self.client.refresh_token = self.refresh_token
        self.client.client_id = self.client_id
        self.client.client_secret = self.client_secret

    def get_activities(self) -> List:
        self.configure_client()
        activities = list(self.client.get_activities())
        return activities