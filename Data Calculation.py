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

#get artists that have survived on bb hot 100 for past 3 weeks
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

def surviving_artists_data(data):
    f = open("surviving_artists.txt", "w" , encoding = "utf-8")
    f.write(json.dumps(data))

#get tracks that have survived on bb hot 100 for past 3 weeks
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

def surviving_tracks_data(data):
    f = open("surviving_tracks.txt", "w" , encoding = "utf-8")
    f.write(json.dumps(data))

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

def track_rank_shifts_data(data):
    f = open("track_rank_shifts.txt", "w" , encoding = "utf-8")
    f.write(json.dumps(data))

def get_mult_appearances_artists(conn1, conn2):

    #create empty dict of artists and their songs (in top 25 this week and 3 weeks ago)
    artists_tracks = {}

    #add artists and their songs to dict (from spotify)
    cur1 = conn1.cursor()
    spotify_tracks = cur1.execute('SELECT title FROM tracks').fetchall()
    spotify_artists = cur1.execute('SELECT artist FROM tracks').fetchall()

    for i in range(25):
        artist = str(spotify_artists[i][0])
        title = str(spotify_tracks[i][0])

        if artist in artists_tracks.keys():
            artists_tracks[artist].append(title)

        else:
            artists_tracks[artist] = [title]
    
        
    #add artists and their songs to dict (from bb)
    cur2 = conn2.cursor()
    bb_tracks= cur2.execute('SELECT title FROM tracks').fetchall()
    bb_artists= cur2.execute('SELECT artist FROM tracks').fetchall()
    
    for i in range(25):
        artist = str(bb_artists[i][0])
        title = str(bb_tracks[i][0])

        if artist in artists_tracks.keys():
            if title not in artists_tracks[artist]:
                artists_tracks[artist].append(title)
        else:
            artists_tracks[artist] = [title] 

    #create empty dict for artists and num of appearances on charts
    artist_appearances = {}
    for artist in artists_tracks:
        if len(artists_tracks[artist]) > 1:
            artist_appearances[artist] = len(artists_tracks[artist])
    
    pprint(artist_appearances)
    return(artist_appearances)

def mult_appearances_artists_data(data):
    f = open("mult_appearances_artists.txt", "w" , encoding = "utf-8")
    f.write(json.dumps(data))
        
def main():
    conn1 = set_connection("tracks.db")
    conn2 = set_connection("billboard_weeks_on_chart.db")
    get_surviving_artists(conn1, conn2)
    surviving_artists_data(get_surviving_artists(conn1, conn2))
    pprint('-----------------------------------------------------')
    conn1 = set_connection("tracks.db")
    conn2 = set_connection("billboard_weeks_on_chart.db")
    get_surviving_tracks(conn1, conn2)
    surviving_tracks_data(get_surviving_tracks(conn1, conn2))
    pprint('-----------------------------------------------------')
    conn1 = set_connection("tracks.db")
    conn2 = set_connection("billboard_weeks_on_chart.db") 
    get_track_rank_shifts(conn1, conn2)
    track_rank_shifts_data(get_track_rank_shifts(conn1, conn2))
    pprint('-----------------------------------------------------')
    conn1 = set_connection("tracks.db")
    conn2 = set_connection("billboard_weeks_on_chart.db")
    get_mult_appearances_artists(conn1, conn2)
    mult_appearances_artists_data(get_mult_appearances_artists(conn1, conn2))

if __name__ == '__main__':
    main()
