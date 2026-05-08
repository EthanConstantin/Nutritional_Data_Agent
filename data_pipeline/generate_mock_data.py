import pandas as pd
import random
import logging
import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- 1. Define the Expected AI Output Schema using Pydantic ---
class Product(BaseModel):
    name: str = Field(description="The brand and name of the product (e.g., 'Presidents Choice Whole Milk')")
    category: str = Field(description="Must be one of: Meat, Produce, Dairy, Pantry, Bakery, Frozen")
    protein_g: int = Field(description="Realistic protein content in grams per serving")
    carbs_g: int = Field(description="Realistic carbohydrate content in grams per serving")
    fats_g: int = Field(description="Realistic fat content in grams per serving")
    base_price: float = Field(description="Realistic base Canadian price (CAD)")

class ProductList(BaseModel):
    products: list[Product]

def generate_ai_products(num_items: int = 100) -> pd.DataFrame:
    """Uses Gemini via AI Studio to synthetically generate realistic grocery items."""
    logging.info(f"Asking Gemini to generate {num_items} realistic grocery items...")
    
    # Initialize the Gemini model via AI Studio (automatically finds GEMINI_API_KEY in .env)
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.7 
    )
    
    structured_llm = llm.with_structured_output(ProductList)
    
    prompt = f"""
    You are an expert nutritionist and Canadian grocery supply chain manager.
    Generate exactly {num_items} distinct, realistic grocery products.
    Ensure a good mix across these categories: Meat, Produce, Dairy, Pantry, Bakery, Frozen.
    Make sure the macros (protein, carbs, fats) make biological sense for the item.
    Make sure the base price reflects realistic Canadian grocery prices in CAD.
    """
    
    try:
        response = structured_llm.invoke(prompt)
        
        formatted_products = []
        for idx, item in enumerate(response.products):
            calories = (item.protein_g * 4) + (item.carbs_g * 4) + (item.fats_g * 9)
            
            formatted_products.append({
                'Product_ID': f"PRD{idx+1:04d}",
                'Name': item.name,
                'Category': item.category,
                'Protein_g': item.protein_g,
                'Carbs_g': item.carbs_g,
                'Fats_g': item.fats_g,
                'Calories': calories,
                '_base_price': item.base_price
            })
            
        return pd.DataFrame(formatted_products)
    
    except Exception as e:
        logging.error(f"Failed to generate data via AI Studio: {e}")
        return pd.DataFrame()

def process_and_export_data(products_df: pd.DataFrame):
    """Normalizes the AI data and exports to CSVs."""
    if products_df.empty:
        return

    logging.info("Normalizing AI data into Stores and Inventory tables...")
    
    stores_df = pd.DataFrame([
        {'Store_ID': 'ST001', 'Brand': 'MockLoblaws', 'Location': 'Oshawa'},
        {'Store_ID': 'ST002', 'Brand': 'MockLoblaws', 'Location': 'Thornhill'}
    ])

    inventory = []
    for _, product in products_df.iterrows():
        for _, store in stores_df.iterrows():
            price_multiplier = random.uniform(0.98, 1.02) 
            if store['Location'] == 'Thornhill':
                price_multiplier += random.uniform(0.04, 0.08) 
                
            final_price = round(product['_base_price'] * price_multiplier, 2)

            inventory.append({
                'Product_ID': product['Product_ID'],
                'Store_ID': store['Store_ID'],
                'Price_CAD': final_price
            })

    inventory_df = pd.DataFrame(inventory)
    final_products_df = products_df.drop(columns=['_base_price'])

    final_products_df.to_csv('products.csv', index=False)
    stores_df.to_csv('stores.csv', index=False)
    inventory_df.to_csv('inventory.csv', index=False)
    
    logging.info(f"Exported {len(final_products_df)} products and {len(inventory_df)} inventory records to CSVs.")

if __name__ == "__main__":
    parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    load_dotenv(dotenv_path=os.path.join(parent_dir, '.env'))
    
    raw_ai_products = generate_ai_products(num_items=100)
    process_and_export_data(raw_ai_products)