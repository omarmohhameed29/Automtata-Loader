import os
from dotenv import load_dotenv
import psycopg2
import pandas as pd
from scrape import *

# Load environment variables
load_dotenv()


try:
    # Connect to PostgreSQL
    cnx = psycopg2.connect(
        user=os.getenv("PGUSER"),
        password=os.getenv("PGPASSWORD"),
        host=os.getenv("PGHOST"),
        port=os.getenv("PGPORT"),
        database=os.getenv("PGDATABASE")
    )
    
    cursor = cnx.cursor()
    
    print("Connected successfully!")
except Exception as e:
    print("Connection failed:", e)
