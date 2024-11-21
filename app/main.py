#!/usr/bin/env python3

from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
import mysql.connector
from mysql.connector import Error
import json
import os


DBHOST = "ds2022.cqee4iwdcaph.us-east-1.rds.amazonaws.com"
DBUSER = "ds2022"
DBPASS = os.getenv('DBPASS')
DB = "atv7xh"

# db = mysql.connector.connect(user=DBUSER, host=DBHOST, password=DBPASS, database=DB, ssl_disabled=True)
# cur=db.cursor()

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
def get_db_connection():
    db = mysql.connector.connect(
        host=DBHOST,
        user=DBUSER,
        password=DBPASS,
        database=DB
    )
    cursor = db.cursor(dictionary=True)  # Fetch rows as dictionaries
    return db, cursor

@app.get('/genres')
async def get_genres():
    # db.cmd_refresh(refresh)
    db = mysql.connector.connect(user=DBUSER, host=DBHOST, password=DBPASS, database=DB)
    cur = db.cursor()
    query = "SELECT * FROM genres ORDER BY genreid;"
    try:    
        db, cur = get_db_connection()  # Ensure this function is correctly implemented
        cur.execute(query)
        results = cur.fetchall()  # Fetch all rows
        return {"genres": results}  # Return the results as JSON
    except Error as e:
        print("MySQL Error: ", str(e))
        cur.close()
        db.close()
        return {"Error": "MySQL Error: " + str(e)}

@app.get('/songs')
async def get_genres():
    # db.cmd_refresh(refresh)
    db = mysql.connector.connect(user=DBUSER, host=DBHOST, password=DBPASS, database=DB)
    cur = db.cursor()
    query = "SELECT songs.title, songs.album, songs.artist, songs.year, songs.file, songs.image, genres.genre FROM songs JOIN genres WHERE songs.genre = genres.genreid;"
    try:
        cur.execute(query)
        results = cur.fetchall()  # Fetch all rows as dictionaries
        return{"songs": results}
    except Error as e:
        return{"Error": f"MySQL Error: {str(e)}"}
    finally:
        if 'cur' in locals() and cur:
            cur.close()
        if 'db' in locals() and db.is_connected():
            db.close()

