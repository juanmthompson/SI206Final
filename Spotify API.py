import json
import sqlite3
import csv
import os
import requests

import matplotlib.pyplot as plt
import numpy as np

os.environ['SPOTIPY_CLIENT_ID']='7e8aa42287834331ab4df141ea09cf4b'
os.environ['SPOTIPY_CLIENT_SECRET']='2352429b6bd54ddab121fbb87ac98ac8'

GRAMMYs_pl_id = 'spotify:playlist:37i9dQZF1DX5FyxM4IcLn6'

from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import sys
from pprint import pprint




def get_playlist(playlist):

    if len(sys.argv) > 1:
        search_str = sys.argv[1]
    else:
        search_str = playlist

    sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
    result = sp.search(search_str)
    pprint(result['tracks'])
    #pprint(type(result))
    




#Pull artist names and track titles from playlist
def get_tracks(pl_id):
    sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

    #pl_id = 'spotify:playlist:37i9dQZF1DX5FyxM4IcLn6'
    offset = 0

    response = sp.playlist_tracks(pl_id, fields= None, limit=None, offset = offset, market=None)

    tracks_list = []
    for track in response['items']:
            
        title = track['track']['name']
        artist = track['track']['album']['artists'][0]['name']
        tracks_list.append((title, artist))
        

    
    return tracks_list


#initialize database, define conn and cur
def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn



def addData(conn, cur, track_data):


    #create tracks table

    command1 = """ CREATE TABLE IF NOT EXISTS
    tracks(title TEXT, artist TEXT)"""
    cur.execute(command1)

    #add to tracks

    for i in range(len(track_data)):
        cur.execute("INSERT INTO tracks VALUES (?, ?)", (track_data[i][0], track_data[i][1])) #+ str(tracks_list[i][0]) + ' ' + str(tracks_list[i][1]))

    conn.commit()



def main():
    cur, conn = setUpDatabase('tracks.db') 
    track_data = get_tracks('37i9dQZF1DX5FyxM4IcLn6')
    pprint(track_data)
    pprint(len(track_data))
    addData(conn, cur, track_data)

if __name__ == '__main__':
    main()
