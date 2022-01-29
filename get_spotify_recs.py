import spotipy
import json
import requests
import os

from dotenv import load_dotenv
load_dotenv()

# set SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET
spotify_access_token = os.getenv("SPOTIFY_ACCESS_TOKEN") # expires every hour

from spotipy.oauth2 import SpotifyClientCredentials
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

spotify_base_url = "https://api.spotify.com/v1"
spotify_user_id="222xt6qcjx3zsvrmhmx3nkb2i"

def search_spotify_track(track, artist):
    """
    looks up a given track on spotify

    :param track: name of track
    :param artist: name of artist

    :return: track id and track uri
    """ 
    search_url = f"https://api.spotify.com/v1/search?q={track}%20{artist}&type=track%2Cartist&market=US&limit=1"
    headers = {"Accept" : "application/json",
        "Content-Type" : "application/json",
        "Authorization" : f"Bearer {spotify_access_token}"}

    response = requests.get(search_url, headers = headers)
    response_json = response.json()
    try:
        track_id = response_json["tracks"]["items"][0]["id"]
        track_uri = response_json["tracks"]["items"][0]["uri"]
    except:
        return None
    return track_id, track_uri

def search_spotify_artist(artist):
    """
    looks up a given artist on spotify

    :param track: name of artist

    :return: artist id and artist uri
    """ 
    search_url = f"https://api.spotify.com/v1/search?q={artist}&type=artist&market=US&limit=1"
    headers = {"Accept" : "application/json",
        "Content-Type" : "application/json",
        "Authorization" : f"Bearer {spotify_access_token}"}

    response = requests.get(search_url, headers = headers)
    response_json = response.json()
    try:
        artist_id = response_json["artists"]["items"][0]["id"]
        artist_uri = response_json["artists"]["items"][0]["uri"]
    except:
        return None
    return artist_id, artist_uri

def get_spotify_recommendations(seed_artists_list, seed_genres_string, seed_tracks_list, target_key, target_tempo):
    """
    provides a list on recommended tracks based on a seed and a given set of params

    :param seed_artists_list: seed list of artists
    :param seed_genres_list: seed list of genres
    :param seed_tracks_list: seed list of tracks
    :param target_key: desired key
    :param target_tempo: desired tempo

    :return: a list of recommended tracks
    """ 
    seed_artists_string = "%2C".join(seed_artists_list)
    #seed_genres_string = "%2C".join(seed_genres_list)
    seed_tracks_string = "%2C".join(seed_tracks_list)
    get_spotify_recommendations_url = f"https://api.spotify.com/v1/recommendations?market=US&seed_artists={seed_artists_string}&seed_genres={seed_genres_string}&seed_tracks={seed_tracks_string}&target_key={target_key}&target_tempo={target_tempo}"

    headers = {"Accept" : "application/json",
        "Content-Type" : "application/json",
        "Authorization" : f"Bearer {spotify_access_token}"}

    response = requests.get(get_spotify_recommendations_url, headers = headers)
    response_json = response.json()
    recommended_tracks_list = response_json["tracks"]
    return recommended_tracks_list

def create_spotify_playlist(name, description, public):
    """
    creates an empty playlist on spotify

    :param name: name of playlist
    :param description: description of playlist
    :param public: true if playlist is public, false otherwise

    :return: playlist id of newly created playlist
    """ 
    create_playlist_url = f"{spotify_base_url}/users/{spotify_user_id}/playlists"

    headers = {"Accept" : "application/json",
        "Content-Type" : "application/json",
        "Authorization" : f"Bearer {spotify_access_token}"}

    data = json.dumps({"name" : name, 
        "description" : description, 
        "public" : public})

    response = requests.post(create_playlist_url, headers = headers, data = data) 
    response_json = response.json()
    playlist_id = response_json["id"] 
    return playlist_id

def add_to_spotify_playlist(playlist_id, track_uri):
    """
    adds a track to an existing spotify playlist

    :param playlist_id: id of playlist to be added to
    :param track_uri: uri of track to be added

    :return: playlist id of newly created playlist
    """ 
    add_to_spotify_playlist_url = f"{spotify_base_url}/playlists/{playlist_id}/tracks"

    headers = {"Accept" : "application/json",
        "Content-Type" : "application/json",
        "Authorization" : f"Bearer {spotify_access_token}"}

    data = json.dumps({"uris" : [track_uri], 
        "position" : 0})

    response = requests.post(add_to_spotify_playlist_url, headers = headers, data = data) 
    response_json = response.json()
    snapshot_id = response_json["snapshot_id"]
    return snapshot_id

def get_track_audio_features(track_id):
    """
    provides the key and tempo of a given track

    :param track_id: id of track

    :return: key, tempo of track
    """
    get_track_audio_features_url = f"https://api.spotify.com/v1/audio-features/{track_id}"

    headers = {"Accept" : "application/json",
        "Content-Type" : "application/json",
        "Authorization" : f"Bearer {spotify_access_token}"}

    response = requests.get(get_track_audio_features_url, headers = headers)
    response_json = response.json()
    key = response_json["key"]
    tempo = response_json["tempo"]
    return key, tempo

# arbitrary values
track_id_1 = search_spotify_track("bad girl", "daya")[0]
track_id_2 = search_spotify_track("perfect", "one direction")[0]
track_id_3 = search_spotify_track("colors", "halsey")[0]
track_id_4 = search_spotify_track("stay", "justin bieber")[0]
track_id_5 = search_spotify_track("one right now", "the weeknd")[0]

artist_id_1 = search_spotify_artist("arijit singh")[0]
artist_id_2 = search_spotify_artist("one direction")[0]
artist_id_3 = search_spotify_artist("halsey")[0]
artist_id_4 = search_spotify_artist("skylar stecker")[0]
artist_id_5 = search_spotify_artist("the weeknd")[0]

seed_tracks_list = [track_id_1, track_id_3]
seed_artists_list = [artist_id_3, artist_id_4]

recommended_tracks_list = get_spotify_recommendations(seed_artists_list, "pop", seed_tracks_list, 5, 100)
recommended_track_uri_list = [track["uri"] for track in recommended_tracks_list]
recommended_track_id_list = [track["id"] for track in recommended_tracks_list]

playlist_id = create_spotify_playlist("spotify-recs", "python-recs", False)

for track_uri in recommended_track_uri_list:
    add_to_spotify_playlist(playlist_id, track_uri)

# DEBUGGING
# print(recommended_tracks_list)
# print(recommended_track_uri_list)
# print(recommended_track_id_list)
# for track_id in recommended_track_id_list:
#     print(get_track_audio_features(track_id))
