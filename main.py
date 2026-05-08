from core_agent.sql_agent import build_grocery_agent
import logging

# Suppress overly verbose Langchain internal logs for a cleaner terminal experience
logging.getLogger("langchain").setLevel(logging.WARNING)

def main():
    print("Initializing Grocery GenAI Agent...")
    try:
        agent = build_grocery_agent()
        print("\n  Agent successfully connected to GCP MySQL Database!")
        print("------------------------------------------------------")
        print("Welcome to the Grocery Agent CLI.")
        print("Ask me about inventory, macros, pricing across locations, etc.")
        print("Type 'exit' or 'quit' to close the program.\n")
        
        while True:
            # 1. Get User Input
            user_input = input("  You: ")
            
            # 2. Check for Exit Command
            if user_input.lower() in ['exit', 'quit', 'q']:
                print("Shutting down agent. Goodbye!")
                break
            
            if not user_input.strip():
                continue
                
            # 3. Invoke Agent
            try:
                print("🤖 Agent is thinking... (Executing SQL)")
                
                response = agent.invoke({"input": user_input})
                
                # Print the final natural language output
                print(f"\n  Answer: {response['output']}\n")
                
            except Exception as e:
                # Catch SQL errors or LLM parsing errors without crashing
                print(f"\nAgent encountered an error processing that request.")
                print(f"Error Details: {str(e)}\n")
                print("Try rephrasing your question.\n")
                
    except Exception as base_error:
        print(f"Failed to start the agent application: {base_error}")

if __name__ == "__main__":
    main()