import collections
import os

import requests

import caching


API_ROOT = "https://anilist.co/api/"
    
@caching.refresh_on_expiration(timeout=3600)
def get_token():
    client_data = {
        'grant_type': 'client_credentials',
        'client_id': os.environ['CLIENT_ID'],
        'client_secret': os.environ['CLIENT_SECRET'],
    }
    resp = requests.post(API_ROOT + "auth/access_token", data=client_data)
    return resp.json()['access_token']
    
@caching.new_request_every(duration=60)
def get_forum_recent():
    query = {'access_token': get_token()}
    resp = requests.get(API_ROOT + "forum/new", params=query)
    return resp.json()
    
def get_doki():
    forum_data = get_forum_recent()['data']
    anime_counter = collections.Counter()
    for post in forum_data:
        anime_tags = post['tags_anime']
        for tag in anime_tags:
            for anime in tag['anime']:
                anime_counter[anime['title_english']] += 1
    return anime_counter