import os
import logging
from dotenv import load_dotenv
from langchain_community.utilities import SQLDatabase

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_db_connection() -> SQLDatabase:
    """Initializes and returns the LangChain SQLDatabase object."""
    
    # Reliably locate the .env file in the parent directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.abspath(os.path.join(current_dir, '..'))
    load_dotenv(os.path.join(parent_dir, '.env'))
    
    database_uri = os.getenv("DATABASE_URI")
    if not database_uri:
        raise ValueError("DATABASE_URI not found. Check your .env file.")
    
    logging.info("Connecting to GCP MySQL Database via LangChain...")
    
    # SQLDatabase wrapper gives the agent read access to the schema
    db = SQLDatabase.from_uri(database_uri)
    
    return db

if __name__ == "__main__":
    # Quick standalone test
    db = get_db_connection()
    print(f"Connected successfully! Found tables: {db.get_usable_table_names()}")