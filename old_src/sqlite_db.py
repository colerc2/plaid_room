#!/usr/bin/python

import sqlite3

class PlaidRoomDatabase():
    def __init__(self, db_name=None):
        self.db = sqlite3.connect(db_name)
        self.db_cursor = self.db.cursor()
        
        #create inventory db
        self.db_cursor.execute("""CREATE TABLE IF NOT EXISTS inventory
        (upc text, artist text, title text, format text, price real, price_paid real, new_used text, distributor text, label text, genre text, year integer, date_added text, discogs_release_number integer, real_name text, profile text, variations text, aliases text, track_list text, notes text, id integer primary key autoincrement)
        """)

        #TODO create history db

    def execute(self, command):
        
