from langchain_community.agent_toolkits import create_sql_agent
from core_agent.db_connection import get_db_connection
from core_agent.llm_config import get_llm

def build_grocery_agent():
    """Compiles the SQL Database and LLM into a LangChain SQL Agent."""
    
    db = get_db_connection()
    llm = get_llm()
    
    # This maps my specific business logic for the agent.
    CUSTOM_PREFIX = """
    You are an expert Data Analyst for a Canadian grocery chain. 
    You are interacting with a MySQL database.
    
    CRITICAL SCHEMA INSTRUCTIONS:
    1. 'inventory' is the central join table. It connects 'products' (via Product_ID) to 'stores' (via Store_ID).
    2. If a user asks for pricing in a specific location (e.g., "Oshawa" or "Thornhill"), you MUST:
       - Query the 'stores' table to find the Store_ID for that location.
       - Join 'stores' to 'inventory' on Store_ID.
       - Join 'inventory' to 'products' on Product_ID to get the product details and price.
    3. Pricing varies by location. Never assume a price is universal; always check the inventory table for the specific store.
    4. If the user asks for macro-specific recommendations (e.g., "high protein", "low calorie", "keto-friendly"), prioritize filtering and sorting by the Protein_g, Carbs_g, Fats_g, or Calories columns in the 'products' table.
    5. Always return prices formatted in CAD (e.g., $4.99).
    
    Use the tools provided to inspect the tables, write the query, and execute it. 
    Double-check your SQL joins before executing.
    """
    
    # create_sql_agent handles the injection of the SQL Toolkit (tools for checking tables, querying, etc.)
    agent_executor = create_sql_agent(
        llm=llm,
        db=db,
        prefix=CUSTOM_PREFIX,
        verbose=True, # Set to True so you can watch its "thought process" in the terminal
        agent_type="zero-shot-react-description" 
    )
    
    return agent_executor