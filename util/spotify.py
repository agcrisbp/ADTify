from base64 import b64encode

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

import requests
import json
import os
import random

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_SECRET_ID = os.getenv("SPOTIFY_SECRET_ID")
BASE_URL = os.getenv("BASE_URL")

REDIRECT_URI = "{}/callback".format(BASE_URL)

# scope user_top_read,user-read-currently-playing,user-read-recently-played
SPOTIFY_URL_REFRESH_TOKEN = "https://accounts.spotify.com/api/token"

SPOTIFY_URL_NOW_PLAYING = (
    "https://api.spotify.com/v1/me/player/currently-playing?additional_types=track,episode"
)
SPOTIFY_URL_RECENTLY_PLAY = "https://api.spotify.com/v1/me/player/recently-played?limit=1"

SPOTIFY_URL_GENERATE_TOKEN = "https://accounts.spotify.com/api/token"

SPOTIFY_URL_USER_INFO = "https://api.spotify.com/v1/me"

SPOTIFY_URL_USER_TOP_READ = "https://api.spotify.com/v1/me/top/tracks"

SPOTIFY_URL_PLAYLIST_READ_PRIVATE = "https://api.spotify.com/v1/me/playlists"

SPOTIFY_URL_PLAYLIST_READ_COLLABORATIVE = "https://api.spotify.com/v1/users/8glrlrg13vyc6hu8tgw6sfvez/playlists"


def get_authorization():

    return b64encode(f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_SECRET_ID}".encode()).decode("ascii")


def generate_token(authorization_code):

    data = {
        "grant_type": "authorization_code",
        "redirect_uri": REDIRECT_URI,
        "code": authorization_code,
    }

    headers = {"Authorization": "Basic {}".format(get_authorization())}

    response = requests.post(SPOTIFY_URL_GENERATE_TOKEN, data=data, headers=headers)
    response_json = response.json()

    return response_json


def refresh_token(refresh_token):

    data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
    }

    headers = {"Authorization": "Basic {}".format(get_authorization())}

    response = requests.post(SPOTIFY_URL_REFRESH_TOKEN, data=data, headers=headers)
    response_json = response.json()

    return response_json


def get_user_profile(access_token):

    headers = {"Authorization": "Bearer {}".format(access_token)}

    response = requests.get(SPOTIFY_URL_USER_INFO, headers=headers)
    response_json = response.json()

    return response_json


def get_recently_play(access_token):

    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(SPOTIFY_URL_RECENTLY_PLAY, headers=headers)

    if response.status_code == 204:
        return {}

    response_json = response.json()
    return response_json


def get_now_playing(access_token):
    """
    Fetch the currently playing track or episode.
    """
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(SPOTIFY_URL_NOW_PLAYING, headers=headers)

    if response.status_code == 204:
        return {}  # No content playing

    response_json = response.json()

    # Handle both tracks and episodes
    if "item" in response_json:
        item = response_json["item"]
        if item["type"] == "episode":  # Podcast episode
            return {
                "is_playing": response_json["is_playing"],
                "progress_ms": response_json["progress_ms"],
                "episode": {
                    "name": item["name"],
                    "show": item["show"]["name"],
                    "description": item["description"],
                    "release_date": item["release_date"],
                    "external_urls": item["external_urls"],
                    "duration_ms": item["duration_ms"],
                    "images": item.get("images") or item["show"].get("images"),
                },
            }
        elif item["type"] == "track":  # Music track
            return {
                "is_playing": response_json["is_playing"],
                "progress_ms": response_json["progress_ms"],
                "track": {
                    "name": item["name"],
                    "artists": item["artists"],
                    "album": item["album"],
                    "external_urls": item["external_urls"],
                    "duration_ms": item["duration_ms"],
                    "images": item["album"]["images"],
                },
            }

    return {}  # Fallback if no valid item is found


def get_recently_play(access_token):
    """
    Fetch the most recently played track or episode.
    """
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(SPOTIFY_URL_RECENTLY_PLAY, headers=headers)

    if response.status_code == 204:
        return {}  # No recent playback found

    response_json = response.json()

    if "items" in response_json and response_json["items"]:
        item = response_json["items"][0]["track"]
        if item["type"] == "episode":  # Podcast episode
            return {
                "played_at": response_json["items"][0]["played_at"],
                "episode": {
                    "name": item["name"],
                    "show": item["show"]["name"],
                    "description": item["description"],
                    "release_date": item["release_date"],
                    "external_urls": item["external_urls"],
                    "duration_ms": item["duration_ms"],
                    "images": item.get("images") or item["show"].get("images"),
                },
            }
        elif item["type"] == "track":  # Music track
            return {
                "played_at": response_json["items"][0]["played_at"],
                "track": {
                    "name": item["name"],
                    "artists": item["artists"],
                    "album": item["album"],
                    "external_urls": item["external_urls"],
                    "duration_ms": item["duration_ms"],
                    "images": item["album"]["images"],
                },
            }

    return {}  # Fallback if no valid item is found
    
def get_user_top_read(access_token):

    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(SPOTIFY_URL_USER_TOP_READ, headers=headers)

    if response.status_code == 204:
        return {}

    response_json = response.json()
    return response_json

def get_playlist_read_private(access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(SPOTIFY_URL_PLAYLIST_READ_PRIVATE, headers=headers)

    if response.status_code == 204:
        return {}

    response_json = response.json()
    return response_json

def get_playlist_read_collaborative(access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(SPOTIFY_URL_PLAYLIST_READ_COLLABORATIVE, headers=headers)

    if response.status_code == 204:
        return {}

    response_json = response.json()
    return response_json