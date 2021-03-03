'''
Created on 28.12.2020
Provides the database API
'''
import abc
from datetime import datetime
import sqlite3, os, time
import json

DEFAULT_DB = 'mydb.db'


# DEFAULT_SCHEMA = 'db/schema.sql'
# DEFAULT_DATA = 'db/data.sql'

class Engine(object):
    def __init__(self, db_path=None):
        super(Engine, self).__init__()
        if db_path is not None:
            self.db_path = db_path
        else:
            self.db_path = DEFAULT_DB

    def connect(self):
        return Connection(self.db_path)


class Connection(object):

    def __init__(self, db_path):
        super(Connection, self).__init__()
        self.con = sqlite3.connect(db_path)

    def close(self):
        if self.con:
            self.con.commit()
            self.con.close()

    def foreign_key(self):
        keys_on = 'PRAGMA foreign_keys = ON'
        try:
            cur = self.con.cursor()
            cur.execute(keys_on)
            return True
        except sqlite3.Error as excp:
            print("Error %s:" % excp.args[0])
            return False

    '''
    DEVICES
    '''

    def device_object(self, row):
        return {
            'id': row['id'],
            'device_name': row['device_name'],
            'topic': row['topic'],
            'location': row['location']
        }

    def create_device(self, device_name, topic, location):
        query = 'INSERT INTO device_info(device_name, topic, location) VALUES(?,?,?)'
        self.foreign_key()
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()
        pvalue = (device_name, topic, location)
        cur.execute(query, pvalue)
        self.con.commit()
        deviceid = cur.lastrowid
        if cur.rowcount < 1:
            return False
        return deviceid

    def get_device(self, device_name):
        query = 'SELECT * FROM device_info WHERE device_name = ?'
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()
        pvalue = (device_name,)
        cur.execute(query, pvalue)
        rows = cur.fetchall()
        if len(rows) is 0:
            return None
        devices = []
        for row in rows:
            device = self.device_object(row)
            devices.append(device)
        return devices

    def update_device(self, device_name, topic):
        query = 'UPDATE members SET topic =? WHERE device_name =?'
        self.foreign_key()
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()
        pvalue = (topic, device_name)
        cur.execute(query, pvalue)
        self.con.commit()
        if cur.rowcount < 1:
            return None
        return device_name

    def delete_member(self, device_name):
        query = 'DELETE FROM device_info WHERE device_name = ?'
        self.foreign_key()
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()
        pvalue = (device_name,)
        cur.execute(query, pvalue)
        self.con.commit()
        if cur.rowcount < 1:
            return False
        return True

