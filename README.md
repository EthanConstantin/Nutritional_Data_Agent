# GenAI Grocery Data Agent

An LLM agent built to translate natural language into complex SQL queries across a multi-location Canadian grocery database. 

This project bridges the gap between unstructured human inquiries and structured relational data, enabling users to instantly filter inventory, compare regional pricing, and optimize for specific macro-nutritional goals without writing a single line of SQL.

##  Architecture Overview

The system is decoupled into two distinct layers to mimic a realistic production environment:

1. **The ETL Pipeline (`/data_pipeline`):** Programmatically generates synthetic, biologically accurate grocery data using Gemini 2.5 Flash. It normalizes this data into three tables (`products`, `stores`, `inventory`) and pushes it to a managed Google Cloud Platform (GCP) MySQL instance.
2. **The Agentic Layer (`/core_agent`):** Utilizes LangChain and Gemini 2.5 Flash (set to 0.1 temperature for deterministic logic) to autonomously orchestrate multi-table `JOIN` operations based on geographic and nutritional semantic triggers.

```text
/genai-grocery-agent
├── .env                        # Credentials (URI, API Key)
├── main.py                     # Root CLI interactive loop
├── /data_pipeline              
│   ├── generate_mock_data.py   # AI-aided CSV synthetic data generation
│   └── setup_database.py       # SQL Ingestion via SQLAlchemy to GCP
└── /core_agent                 
    ├── db_connection.py        # LangChain SQLDatabase initialization
    ├── llm_config.py           # Gemini 2.5 Flash configuration
    └── sql_agent.py            # Agent compilation & System Prompt engineering
```
##  Tech Stack
Core: Python, Pandas

GenAI / Orchestration: LangChain, Google Gemini 2.5 Flash, Google AI Studio

Database & Infrastructure: MySQL, Google Cloud Platform (Cloud SQL), SQLAlchemy, PyMySQL

##  Example Queries
The agent is engineered to handle complex logic, including regional price variations (e.g., automated markups in Thornhill vs. Oshawa) and macro-nutrient prioritization.

User: "What is the cheapest high-protein meat available in Oshawa?"

Agent Action: Queries the stores table for Oshawa's ID -> Joins to inventory -> Joins to products -> Filters by Category='Meat' -> Sorts by Protein_g descending and Price_CAD ascending.

Output: "The cheapest high-protein meat in Oshawa is the generic Chicken Breast (PRD042), containing 31g of protein for $6.49 CAD."

User: "If I'm in Thornhill, how much would it cost to buy a dozen eggs, whole milk, and sourdough bread?"

Agent Action: Maps semantic items to closest Product_ID -> Filters inventory explicitly by Thornhill's Store_ID to account for regional markups -> Sums total.

Output: "In Thornhill, a dozen eggs, whole milk, and sourdough bread will cost you a total of $14.85 CAD."

##  Local Setup & Execution
Clone the repository.

Install dependencies: pip install -r requirements.txt

Create a .env file in the root directory with your credentials:

```
GEMINI_API_KEY="your_google_ai_studio_key"
DATABASE_URI="mysql+pymysql://user:password@<GCP_IP>:3306/grocery_db"
```
Run the interactive CLI:
```
python main.py
```