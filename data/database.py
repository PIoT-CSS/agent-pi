"""
module contains function to get device id.
"""
import sqlite3
import uuid

class Database:
    """
    A class to obtain id of the device from the database, if not 
    generate ID

    Methods
    -------
    get_id(self):
        connect to sqllite, gets id of the device, if table/id doesn't exist,
        it will create table and generate id.
    """

    def get_id(self):
        conn = sqlite3.connect('./rbpi-rmit-iot.db')
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS info (id TEXT PRIMARY KEY)")

        c.execute("SELECT id FROM info")
        fetch = c.fetchone()
        FETCH_ID = fetch[0] if fetch is not None else None

        if(FETCH_ID is None):
            ID = str(uuid.uuid4()).replace('-', '')
            print('initialise ' + ID)
            c.execute("INSERT INTO info (id) VALUES (?)", [ID])
        else:
            ID = FETCH_ID

        conn.commit()
        conn.close()
        return ID

