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
        database=os.getenv("PGDATABASE"),
        sslmode="require"  # Ensures a secure connection
    )
    
    cursor = cnx.cursor()
    
    print("Connected successfully!")

    # List of functions returning DataFrames
    functions = [
        league_table, top_scorers, detail_top, player_table, 
        all_time_table, all_time_winner_club, top_scorers_seasons, goals_per_season
    ]

    for fun in functions:
        function_name = fun.__name__  # Get function name for table name
        try:
            result_df = fun()  # Call function
            if isinstance(result_df, pd.DataFrame):  # Ensure it's a DataFrame
                # Convert DataFrame to list of tuples
                data_tuples = [tuple(x) for x in result_df.to_numpy()]
                
                # Generate column names for SQL query
                columns = ", ".join(result_df.columns)
                placeholders = ", ".join(["%s"] * len(result_df.columns))
                create_table_query = f"""
                CREATE TABLE IF NOT EXISTS {function_name} (
                    {', '.join([f'{col} TEXT' for col in result_df.columns])}
                );
                """
                insert_query = f"INSERT INTO {function_name} ({columns}) VALUES ({placeholders});"
                
                # Create table if not exists
                cursor.execute(create_table_query)
                
                # Insert data
                cursor.executemany(insert_query, data_tuples)
                cnx.commit()  # Commit transaction
                
                print(f'✅ Pushed data for {function_name}')
            else:
                print(f'⚠️ {function_name} did not return a DataFrame')
        except Exception as e:
            print(f'❌ Failed to push {function_name}: {e}')
            cnx.rollback()  # Rollback in case of error

    # Close connection
    cursor.close()
    cnx.close()
    print("Database connection closed.")

except Exception as e:
    print("Connection failed:", e)


