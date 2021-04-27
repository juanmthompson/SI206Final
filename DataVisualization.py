import json
import requests
import spotipy
import os
import sqlite3
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
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

def surviving_artists_piechart(conn1, conn2):
    # Creating dataset
    surviving_p = ((get_surviving_artists(conn1, conn2))[1])
    dead_p = 100 - int(surviving_p)
    print(surviving_p)
    print(dead_p)
    y = np.array([surviving_p, dead_p])
    mylabels = ["artists still on the charts after 3 weeks", "artists off the charts"]

    plt.pie(y, labels = mylabels)
    plt.legend()
    plt.show()

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

def surviving_tracks_piechart(conn1, conn2):
    # Creating dataset
    surviving_p = (get_surviving_tracks(conn1, conn2)[1])
    dead_p = 100 - surviving_p
    print(surviving_p)
    print(dead_p)
    y = np.array([surviving_p, dead_p])
    mylabels = ["songs still on the charts after 3 weeks", "songs off the charts"]

    plt.pie(y, labels = mylabels)
    plt.legend()
    plt.show()

def get_track_rank_shifts(conn1, conn2):
    track_rank_shifts = {}
    #get spotify titles and ranks (top 25 this week)
    cur1 = conn1.cursor()
    spotify_tracks = cur1.execute('SELECT title FROM tracks').fetchall()
    spotify_ranks = cur1.execute('SELECT rank FROM tracks').fetchall()
    spotify_tracks_ranks = {}
    for i in range(25):
        spotify_tracks_ranks[(str(spotify_tracks[i][0]))] = str(spotify_ranks[i][0])
        
    #get billboard titles and ranks (top 25 three weeks ago)
    cur2 = conn2.cursor()
    bb_tracks= cur2.execute('SELECT title FROM tracks').fetchall()
    bb_ranks= cur2.execute('SELECT rank FROM tracks').fetchall()
    bb_tracks_ranks = {}
    for i in range(25):
        bb_tracks_ranks[(str(bb_tracks[i][0]))] = str(bb_ranks[i][0])
        
    #combine dicts to form a new dict with titles and rank differences(shifts)
    for key in spotify_tracks_ranks:
        if key in bb_tracks_ranks:

            track_rank_shifts[key] = (int(bb_tracks_ranks[key]) - int(spotify_tracks_ranks[key]))

    pprint(track_rank_shifts)
    return(track_rank_shifts)
    


        











def main():
    conn1 = set_connection("tracks.db")
    conn2 = set_connection("billboard_weeks_on_chart.db")
    get_surviving_artists(conn1, conn2)
    surviving_artists_piechart(conn1, conn2)

    pprint('-----------------------------------------------------')
    conn1 = set_connection("tracks.db")
    conn2 = set_connection("billboard_weeks_on_chart.db")
    get_surviving_tracks(conn1, conn2)
    surviving_tracks_piechart(conn1, conn2)
    

    pprint('-----------------------------------------------------')
    conn1 = set_connection("tracks.db")
    conn2 = set_connection("billboard_weeks_on_chart.db") #billboard_rankings.db
    get_track_rank_shifts(conn1, conn2)
    rank_shift_graph(conn1, conn2) 

if __name__ == '__main__':
    main()
