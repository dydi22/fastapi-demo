#!/usr/bin/env python3

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mysql.connector import Error
import mysql.connector
import os

# Database Configuration
DBHOST = "ds2022.cqee4iwdcaph.us-east-1.rds.amazonaws.com"
DBUSER = "ds2022"
DBPASS = os.getenv('DBPASS')  # Securely fetch password from environment variable
DB = "atv7xh"

# Initialize FastAPI Application
app = FastAPI()

# CORS Middleware Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (adjust as necessary for production)
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Helper Function to Get Database Connection
def get_db_connection():
    try:
        db = mysql.connector.connect(
            host=DBHOST,
            user=DBUSER,
            password=DBPASS,
            database=DB,
            ssl_disabled=True
        )
        cursor = db.cursor(dictionary=True)  # Fetch rows as dictionaries
        return db, cursor
    except Error as e:
        raise RuntimeError(f"Database connection failed: {str(e)}")

# Route to Fetch All Genres
@app.get('/genres')
async def get_genres():
    query = "SELECT * FROM genres ORDER BY genreid;"
    try:
        db, cur = get_db_connection()
        cur.execute(query)
        results = cur.fetchall()
        return {"genres": results}
    except Error as e:
        return {"error": f"MySQL Error: {str(e)}"}
    finally:
        if 'cur' in locals() and cur:
            cur.close()
        if 'db' in locals() and db.is_connected():
            db.close()

# Route to Fetch All Songs with Genre Info
@app.get('/songs')
async def get_songs():
    query = """
        SELECT 
            songs.title, 
            songs.album, 
            songs.artist, 
            songs.year, 
            songs.file, 
            songs.image, 
            genres.genre 
        FROM 
            songs 
        JOIN 
            genres 
        ON 
            songs.genre = genres.genreid;
    """
    try:
        db, cur = get_db_connection()
        cur.execute(query)
        results = cur.fetchall()
        return {"songs": results}
    except Error as e:
        return {"error": f"MySQL Error: {str(e)}"}
    finally:
        if 'cur' in locals() and cur:
            cur.close()
        if 'db' in locals() and db.is_connected():
            db.close()
