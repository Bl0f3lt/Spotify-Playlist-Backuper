#!/bin/python3.8
import sqlite3

playlist_Name = input('Enter playlist name: ')
db_Name = ('{}Backup.db'.format(playlist_Name))

con = sqlite3.connect('{}'.format(db_Name))
cur = con.cursor()
for row in cur.execute('SELECT trackName, trackArtist FROM tracks'):
    rowName = str(row)
    rowNameList = list(rowName)
    rowNameList[0] = ""
    rowNameList[1] = ""
    rowNameList[-1] = ""
    rowNameList[-2] = ""
    rowNameList[-3] = ""
    rowName = "".join(rowNameList)
    print(rowName)
