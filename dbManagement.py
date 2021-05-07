import os
import sqlite3

DEFAULT_DB_PATH = os.path.join(os.path.dirname(__file__), 'local_database.sqlite3')


def db_connect(db_path=DEFAULT_DB_PATH, isThreading=0):
    conn = None
    try:
        if isThreading:
            conn = sqlite3.connect(db_path, isolation_level=None)
            conn.execute('pragma journal_mode=wal;')
        else:
            conn = sqlite3.connect(db_path)
    except sqlite3.Error as error:
        print("Failed to connect to the database - ", error)

    return conn


def create_table(cursor, tableSQLcode):
    try:
        cursor.execute(tableSQLcode)
    except sqlite3.Error as error:
        print("Failed to proceed table sql code: ", error)


def create_all_required_tables(connect):    # sets up tables "songs", "movies", "apps"
    cur = connect.cursor()

    songsTbl = """
    CREATE TABLE songs (
        song_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        artist_name VARCHAR(100),
        title VARCHAR(100),
        year INTEGER,
        release VARCHAR(100),
        ingestion_time DATETIME )"""
    create_table(cur, songsTbl)

    moviesTbl = """
        CREATE TABLE movies (
            movie_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            original_title VARCHAR(100),
            original_language VARCHAR(100),
            budget INTEGER,
            is_adult BOOLEAN,
            release_date DATE,
            original_title_normalized VARCHAR(100) )"""
    create_table(cur, moviesTbl)

    appsTbl = """
            CREATE TABLE apps (
                app_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                name VARCHAR(100),
                genre VARCHAR(100),
                rating FLOAT,
                version VARCHAR(100),
                size_bytes INTEGER,
                is_awesome BOOLEAN )"""
    create_table(cur, appsTbl)

    cur.close()


def insert_in_songs(connect, values):   # values is a touple
    cur = connect.cursor()
    try:
        sqliteInsertWithParam = """INSERT INTO songs
                                  (artist_name, title, year, release, ingestion_time) 
                                  VALUES (?, ?, ?, ?, ?);"""    # if _id column is ignored, it will be automatic
        cur.execute(sqliteInsertWithParam, values)
        connect.commit()
    except sqlite3.Error as error:
        print("Failed to insert data into 'songs' table: ", error)

    cur.close()


def insert_in_movies(connect, values):   # values is a touple
    cur = connect.cursor()
    try:
        sqliteInsertWithParam = """INSERT INTO movies
                                  (original_title, original_language, budget, is_adult, 
                                  release_date, original_title_normalized) 
                                  VALUES (?, ?, ?, ?, ?, ?);"""  # if _id column is ignored, it'll be automatic
        cur.execute(sqliteInsertWithParam, values)
        connect.commit()
    except sqlite3.Error as error:
        print("Failed to insert data into 'movies' table: ", error)

    cur.close()


def insert_in_apps(connect, values):   # values is a touple
    cur = connect.cursor()
    try:
        sqliteInsertWithParam = """INSERT INTO apps
                                  (name, genre, rating, version, size_bytes, is_awesome) 
                                  VALUES (?, ?, ?, ?, ?, ?);"""  # if _id column is ignored, it'll be automatic
        cur.execute(sqliteInsertWithParam, values)
        connect.commit()
    except sqlite3.Error as error:
        print("Failed to insert data into 'apps' table: ", error)

    cur.close()


def insert_many_one_type_values(valuesOfType, tblType, dbPath=DEFAULT_DB_PATH):
    dbConnect = db_connect(dbPath, 1)   # the function is rather used in threading, so isThreading=1
    if tblType == 'song':     # in order to use proper functions
        for songInsData in valuesOfType:
            insert_in_songs(dbConnect, songInsData)
    if tblType == 'movie':    # in order to use proper functions
        for movieInsData in valuesOfType:
            insert_in_movies(dbConnect, movieInsData)
    if tblType == 'app':      # in order to use proper functions
        for appInsData in valuesOfType:
            insert_in_apps(dbConnect, appInsData)
    dbConnect.close()
