import pandas as pd
import logging
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def upload_csvs_to_database():
    """Reads normalized CSVs and pushes them to the GCP MySQL instance."""
    
    # 1. Load Environment Variables
    parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    env_path = os.path.join(parent_dir, '.env')
    load_dotenv(dotenv_path=env_path)
    
    database_uri = os.getenv("DATABASE_URI")
    if not database_uri:
        logging.error("DATABASE_URI not found. Please check your .env file.")
        return

    # 2. Check for the CSV files
    try:
        logging.info("Reading CSV files...")
        products_df = pd.read_csv('products.csv')
        stores_df = pd.read_csv('stores.csv')
        inventory_df = pd.read_csv('inventory.csv')
    except FileNotFoundError as e:
        logging.error(f"CSV files not found. Did you run generate_mock_data.py first? Error: {e}")
        return

    # 3. Upload to GCP Cloud SQL
    logging.info("Establishing connection to GCP database...")
    try:
        engine = create_engine(database_uri)
        with engine.connect() as connection:
            logging.info("Connection successful! Pushing DataFrames to SQL...")
            
            # Order matters slightly for mental organization, though pandas to_sql doesn't natively enforce Foreign Keys
            stores_df.to_sql('stores', con=engine, if_exists='replace', index=False)
            logging.info("Successfully wrote 'stores' table.")
            
            products_df.to_sql('products', con=engine, if_exists='replace', index=False)
            logging.info("Successfully wrote 'products' table.")
            
            inventory_df.to_sql('inventory', con=engine, if_exists='replace', index=False)
            logging.info(f"Successfully wrote 'inventory' table with {len(inventory_df)} records.")
            
            logging.info("Database ingestion complete.")
            
    except SQLAlchemyError as e:
        logging.error(f"Database connection or upload failed: {e}")

if __name__ == "__main__":
    upload_csvs_to_database()