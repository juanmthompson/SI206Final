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
    charts_url = 'https://www.billboard.com/charts/hot-100/2021-04-10'
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
    charts_url = 'https://www.billboard.com/charts/hot-100/2021-04-10'
    resp = requests.get(charts_url)
    artist_list = []
    soup = BeautifulSoup(resp.text, 'html.parser')
    names = soup.find_all('span', class_ = 'chart-element__information__artist text--truncate color--secondary')
    for name in names:
        artist_name = name.text.strip()
        if 'Featuring' or 'X' or '&' in artist_name:
            split_name = artist_name.split('Featuring', 1)
            artist_name = split_name[0]
        artist_list.append(artist_name)
    print(artist_list)
    return artist_list

def get_song_rank():
    base_url = 'http://billboard.com'
    charts_url = 'https://www.billboard.com/charts/hot-100/2021-04-10'
    resp = requests.get(charts_url)
    rank_list = []
    soup = BeautifulSoup(resp.text, 'html.parser')
    rank = soup.find_all('span', class_ = 'chart-element__rank__number')
    for ranks in rank:
        rank_list.append(ranks.text.strip())
    #print(rank_list)
    return rank_list

def get_weeks_on_chart():
    base_url = 'http://billboard.com'
    charts_url = 'https://www.billboard.com/charts/hot-100/2021-04-10'
    resp = requests.get(charts_url)
    weeks_list = []
    soup = BeautifulSoup(resp.text, 'html.parser')
    weeks = soup.find_all('span', class_ = 'chart-element__meta text--center color--secondary text--week')
    for week in weeks:
        weeks_list.append(week.text.strip().replace((' WoC'), ''))
    #print(weeks_list)
    return weeks_list

# combine data into tuples for the first table
def first_table():
    song_list = get_song_names()
    artist_list =  get_song_artists()
    rank_list = get_song_rank()
    tuple_list = list(zip(rank_list, song_list, artist_list))
    #pprint(tuple_list)
    return tuple_list

# combine data into tuples for the second table
def second_table():
    song_list = get_song_names()
    artist_list =  get_song_artists()
    weeks_list = get_weeks_on_chart()
    tuple_list = list(zip(song_list, artist_list, weeks_list))
    #pprint(tuple_list)
    return tuple_list

#set up the first database table
def setUp1Database(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

#add to the first database table
def add1Data(conn, cur, ranking_list):
    #create tracks table


    command1 = """ CREATE TABLE IF NOT EXISTS
    tracks(rank INTEGER PRIMARY KEY, title TEXT, artist TEXT)"""
    cur.execute(command1)

    #add to tracks

    for i in range(25): #ASK LUCY
        cur.execute("INSERT INTO tracks VALUES (?, ?, ?)", (ranking_list[i][0], ranking_list[i][1], ranking_list[i][2]))
    conn.commit()
    #results = cur.fetchall()
    #print(results)
    #return results


    weeks_list = second_table()

    #create tracks2 table


    command2 = """ CREATE TABLE IF NOT EXISTS
    tracks2(title TEXT, artist TEXT, weeks TEXT)"""
    cur.execute(command2)

    #add to tracks2

    for i in range(25): #ASK LUCY
        cur.execute("INSERT INTO tracks2 VALUES (?, ?, ?)", (weeks_list[i][0], weeks_list[i][1], weeks_list[i][2]))
    conn.commit()


#set up the second database table
def setUp2Database(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn



# call functions 
def main():
    get_song_names()
    get_song_artists()
    get_song_rank()
    get_weeks_on_chart()
    cur, conn = setUp1Database('billboard_rankings.db') 
    cur, conn = setUp2Database('billboard_weeks_on_chart.db')
    ranking_list = first_table()

    add1Data(conn, cur, ranking_list)


if __name__ == '__main__':
    main()


