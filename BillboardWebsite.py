from bs4 import BeautifulSoup
import requests
import re
import os
import csv
import unittest
import sqlite3
from pprint import pprint

#get top song names
def get_song_names():
    charts_url = 'http://billboard.com/charts/hot-100'
    resp = requests.get(charts_url)
    song_list = []
    soup = BeautifulSoup(resp.text, 'html.parser')
    songs = soup.find_all('span', class_ = 'chart-element__information__song text--truncate color--primary')
    for song in songs:
        song_list.append(song.text.strip())
    #print(song_list)
    return song_list

#get artists of top songs 
def get_song_artists():
    base_url = 'http://billboard.com'
    charts_url = 'http://billboard.com/charts/hot-100'
    resp = requests.get(charts_url)
    artist_list = []
    soup = BeautifulSoup(resp.text, 'html.parser')
    names = soup.find_all('span', class_ = 'chart-element__information__artist text--truncate color--secondary')
    for name in names:
        artist_list.append(name.text.strip())
    #print(artist_list)
    return artist_list

'''def get_song_rank():
    base_url = 'http://billboard.com'
    charts_url = 'http://billboard.com/charts/hot-100'
    resp = requests.get(charts_url)
    rank_list = []
    soup = BeautifulSoup(resp.text, 'html.parser')
    rank = soup.find_all('span', class_ = 'chart-element__rank__number')
    for ranks in rank:
        rank_list.append(rank.strip())
    print(rank_list)
    return rank_list'''

# combine data into tuples
def create_tuples():
    song_list = get_song_names()
    artist_list =  get_song_artists()
    #rank_list = get_song_rank()
    tuple_list = list(zip(song_list, artist_list))
    #pprint(tuple_list)
    return tuple_list

#set up the database
def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

#add to the database
def addData(conn, cur, tuple_list):
    #create tracks table

    command1 = """ CREATE TABLE IF NOT EXISTS
    tracks(title TEXT, artist TEXT)"""
    cur.execute(command1)

    #add to tracks

    for i in range(len(tuple_list)):
        cur.execute("INSERT INTO tracks VALUES (?, ?)", (tuple_list[i][0], tuple_list[i][1])) #+ str(tracks_list[i][0]) + ' ' + str(tracks_list[i][1]))
        conn.commit()
    results = cur.fetchall()
    print(results)
    return results


# call functions 
def main():
    get_song_names()
    get_song_artists()
    #get_song_rank()
    create_tuples()
    cur, conn = setUpDatabase('billboard_top_100.db') 
    tuple_list = create_tuples()
    addData(conn, cur, tuple_list)

if __name__ == '__main__':
    main()


