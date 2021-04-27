import json
import requests
import spotipy
import os
import sqlite3
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
import matplotlib.pyplot as plt
from pprint import pprint


def set_connection(db_file):
    try:
        path = os.path.dirname(os.path.abspath(__file__))
        conn = sqlite3.connect(path+'/'+db_file)
    except:
        print("Couldn't connect to Database")
    return conn

def get_surviving_artists(conn1, conn2):
    surviving_artists = []
    cur1 = conn1.cursor()
    cur2 = conn2.cursor()
    spotify_artists = cur1.execute('SELECT artist FROM tracks').fetchall()
    bb_artists = cur2.execute('SELECT artist FROM tracks2').fetchall()

    for artist in spotify_artists:
        if artist in bb_artists:
            surviving_artists.append(artist[0])
    
    survival_percentage = (len(surviving_artists) / len(spotify_artists)) * 100
    pprint(surviving_artists)
    pprint(str(survival_percentage) + " percent of the artists on Billboard Hot 100 today have been on Billboard Hot 100 for the past three weeks")
    return (surviving_artists, survival_percentage)

def get_surviving_tracks(conn1, conn2):
    surviving_tracks = []
    cur1 = conn1.cursor()
    cur2 = conn2.cursor()
    spotify_tracks = cur1.execute('SELECT title FROM tracks').fetchall()
    bb_tracks= cur2.execute('SELECT title FROM tracks2').fetchall()

    for artist in spotify_tracks:
        if artist in bb_tracks:
            surviving_tracks.append(artist[0])
    
    survival_percentage = (len(surviving_tracks) / len(spotify_tracks)) * 100
    pprint(surviving_tracks)
    pprint(str(survival_percentage) + " percent of the tracks on Billboard Hot 100 today have been on Billboard Hot 100 for the past three weeks")
    return (surviving_tracks, survival_percentage)

def get_track_rank_shifts(conn1, conn2):
    track_rank_shifts = []

    cur1 = conn1.cursor()
    spotify_tracks = cur1.execute('SELECT title FROM tracks').fetchall()
    spotify_ranks = cur1.execute('SELECT rank FROM tracks').fetchall()

    cur2 = conn2.cursor()
    bb_tracks= cur2.execute('SELECT title FROM tracks').fetchall()
    bb_ranks= cur2.execute('SELECT rank FROM tracks').fetchall()

    for i in range(len(spotify_tracks)):
        if spotify_tracks[i] in bb_tracks:
            print(spotify_tracks[i][0])
            print(spotify_ranks[i][0])
            print('------------------')
            print(bb_tracks[i][0])
            print(bb_ranks[i][0])
            print('------------------')
            #shift = int(spotify_ranks[i][0]) - int(bb_ranks[i][0])
            #track_rank_shifts.append((spotify_tracks[i][0], shift))
    
    pprint(track_rank_shifts)
    return(track_rank_shifts)


        











def main():
    conn1 = set_connection("tracks.db")
    conn2 = set_connection("billboard_weeks_on_chart.db")
    get_surviving_artists(conn1, conn2)
    pprint('-----------------------------------------------------')
    conn1 = set_connection("tracks.db")
    conn2 = set_connection("billboard_weeks_on_chart.db")
    get_surviving_tracks(conn1, conn2)
    pprint('-----------------------------------------------------')
    conn1 = set_connection("tracks.db")
    conn2 = set_connection("billboard_weeks_on_chart.db") #billboard_rankings.db
    get_track_rank_shifts(conn1, conn2)

if __name__ == '__main__':
    main()

