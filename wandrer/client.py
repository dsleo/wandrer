from dataclasses import dataclass
from stravalib import Client

@dataclass
class StravaClient:
    access_token: str
    refresh_token: str
    client_id: str
    client_secret: str

    client = Client()

    def configure_client(self):
        self.client.access_token = self.access_token
        self.client.refresh_token = self.refresh_token
        self.client.client_id = self.client_id
        self.client.client_secret = self.client_secret

    def get_activities(self):
        self.configure_client()
        activities = list(self.client.get_activities())
        return activities