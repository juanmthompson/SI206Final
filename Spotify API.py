import json
import sqlite3
import csv
import os
import requests
import matplotlib.pyplot as plt
import numpy as np
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import sys
from pprint import pprint

os.environ['SPOTIPY_CLIENT_ID']='7e8aa42287834331ab4df141ea09cf4b'
os.environ['SPOTIPY_CLIENT_SECRET']='2352429b6bd54ddab121fbb87ac98ac8'


#Pull artist names and track titles from playlist
#Billboard Hot 100 playlist - 6UeSakyzhiEt4NB3UAd6NQ
def get_tracks(pl_id):
    sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

    offset = 0
    response = sp.playlist_tracks(pl_id, fields= None, limit=None, offset = offset, market=None)

    tracks_list = []
    for track in response['items']:
            
        title = track['track']['name']
        if ' (feat.' in title:
            split_title = title.split(' (feat.', 1)
            title = split_title[0]
        artist = track['track']['album']['artists'][0]['name']
        tracks_list.append((title, artist))
        
    return tracks_list


#initialize database, define conn and cur
def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn



def addData(conn, cur, tracks_list): #


    #create tracks table

    command1 = """ CREATE TABLE IF NOT EXISTS
    tracks(rank INTEGER PRIMARY KEY, title TEXT, artist TEXT)"""
    cur.execute(command1)

    #add to tracks

    for i in range(25): #ASK LUCY
        cur.execute("INSERT INTO tracks VALUES (?, ?, ?)", ((i + 1), tracks_list[i][0], tracks_list[i][1])) 

    conn.commit()

    #join spotify table with billboards table

    
    
def joinData(conn, cur):
    cur.execute('SELECT * FROM track_data JOIN tuple_list ON track_data = ranking_list.rank') #ASK LUCY ABOUT ERROR

def main():
    cur, conn = setUpDatabase('tracks.db') 
    track_data = get_tracks('6UeSakyzhiEt4NB3UAd6NQ')
    pprint(track_data)
    pprint(len(track_data))
    addData(conn, cur, track_data)
    joinData(conn, cur)

if __name__ == '__main__':
    main()
