#!/bin/python3.8
from datetime import date
import requests
import sqlite3
import time

def checkPreExistingTrack(playlistName,trackName):
	preExistingTrack = False
	con = sqlite3.connect('{}Backup.db'.format(playlistName))
	cur = con.cursor()
	for row in cur.execute('SELECT trackName FROM tracks'):
		rowName = str(row)
		rowNameList = list(rowName)
		rowNameList[0] = ""
		rowNameList[1] = ""
		rowNameList[-1] = ""
		rowNameList[-2] = ""
		#rowNameList[-3] = ""
		rowName = "".join(rowNameList)
		if rowName == trackName:
			print('{} -- {}'.format(rowName,trackName))
			preExistingTrack = True
			break
	con.commit()
	con.close()
	return(preExistingTrack)
		
def checkFileExists(playlistName):
	preExisting = False
	f = open('playlistsRan.txt','r')
	for x in f:
		if x == playlistName:
			preExisting = True
	f.close()
	return(preExisting)
	

def generateDB(playlistName):
	preExisting = checkFileExists(playlistName)
	if preExisting == False:
		try:
			con = sqlite3.connect('{}Backup.db'.format(playlistName))
			con.commit()
			con.close()
			return(False)
		except:
			return(True)	
	else:
		print('Database Already Found!')
		print('Adding To Existing Database')
		return(True)	

def populateDB(playlistName):
	con = sqlite3.connect('{}Backup.db'.format(playlistName))
	cur = con.cursor()
	try:
		cur.execute('''CREATE TABLE tracks
						(dateBackedUp, trackName, trackArtist)''')
		con.commit()
		con.close()
	except:
		return()

client_id = ''
client_secret = ''

auth_url = 'https://accounts.spotify.com/api/token'

data = {
	'grant_type': 'client_credentials',
	'client_id': client_id,
	'client_secret': client_secret,
}

auth_response = requests.post(auth_url, data=data)
access_token = auth_response.json().get('access_token')

base_url = 'https://api.spotify.com/v1/'

headers = {
	'Authorization': 'Bearer {}'.format(access_token)
}

playlist_id = input('Enter Playlist Id: ')
tracks = {}
numOfTracks = 0
artist_ids = set()
pr = requests.get(base_url + 'playlists/{}/tracks'.format(playlist_id), headers=headers)
pr_data = pr.json()
playlistName = input('Enter Playlist Name: ')
#Making backup database
existingDB = generateDB(playlistName)
if existingDB == False:
	populateDB(playlistName)
con = sqlite3.connect('{}Backup.db'.format(playlistName))
cur = con.cursor()
backupDate = time.strftime('%d-%m-%Y')
#Registering that db has already been created
f = open('playlistsRan.txt', 'a')
f.write('\n')
f.write(playlistName)
f.close()

if pr_data:
	playlist_data = pr_data.get('items')
	for tr in playlist_data:
		track = tr.get('track')
		if track:
			#print(track)
			name = track.get('name')
			artists = track.get('artists')
			for artist in artists:
				artistName = artist.get('name')
			numOfTracks += 1
		#sqlStatement = (''.format(backupDate),''.format(name),''.format(artistName))
		duplicate = checkPreExistingTrack(playlistName,name)
		if duplicate == False:
			cur.execute("INSERT INTO tracks (dateBackedUp, trackName, trackArtist) VALUES (?, ?, ?) ", (backupDate,name,artistName))
		
		#print('{} - {}'.format(name,artistName))
if numOfTracks == 100:
	pr = requests.get(base_url + 'playlists/{}/tracks/?offset=100'.format(playlist_id), headers=headers)
	pr_data = pr.json()
	if pr_data:
		playlist_data = pr_data.get('items')
		for tr in playlist_data:
			track = tr.get('track')
			if track:
				name = track.get('name')
				artists = track.get('artists')
				for artist in artists:
					artistName = artist.get('name')
				numOfTracks += 1
			#sqlStatement = (''.format(backupDate),''.format(name),''.format(artistName))
			duplicate = checkPreExistingTrack(playlistName,name)
			if duplicate == False:
				cur.execute("INSERT INTO tracks (dateBackedUp, trackName, trackArtist) VALUES (?, ?, ?) ", (backupDate,name,artistName))
			#print('{} - {}'.format(name,artistName))
con.commit()
con.close()
#print(numOfTracks)
#print(tracks)
#f = open('{}-backup.json'.format(playlistName), 'x')
#f.close()
#with open('{}-backup.json'.format(playlistName), 'w') as f:
#	json.dump(tracks, f)
#f.close()
#tracks.append({'name': '{}'.format(name), 'artist': '{}'.format(artistName)})
