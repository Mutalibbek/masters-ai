import openai
from openai import OpenAI
from dotenv import load_dotenv
import os
from tenacity import retry, wait_random_exponential, stop_after_attempt
import sqlite3
import json

# Load environment variables
load_dotenv()

# Constants
MODEL = "gpt-4"
DATABASE = "buildings_with_coordinates_2.db"
USER_MESSAGE = "Hi, calculate the total buildings for each city"

# Initialize OpenAI client
openai.api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()

# Database schema
database_schema = """
Table: buildings_with_coordinates_2
Columns: project_no, city, building_name, price_per_sqm, min_price_per_sqm, max_price_per_sqm, project_status, address, company,
accommodation_class, stories, ceiling_height, building_type, decoration, number_of_apartments,
kitchen, facade, apartments_for_sale, parking, heating, elevator, nearby, inside, safety,
description, source_website, purchase_conditions, payment_options, location_id, price_float,
ceiling_height_float, stories_float, full_address, latitude, longitude
"""

# Tools for function calling
tools = [
    {
        "type": "function",
        "function": {
            "name": "query_database",
            "description": "Query a SQLite database to retrieve real estate information.",
            "strict": True,
            "parameters": {
                "type": "object",
                "properties": {
                    "sql_query": {
                        "type": "string",
                        "description": "The SQL query to execute."
                    }
                },
                "required": ["sql_query"],
                "additionalProperties": False
            }
        }
    }
]

# Step 1: Function to query the database
def query_database(sql_query: str) -> list:
    try:
        # Connect to the SQLite database
        with sqlite3.connect(DATABASE) as connection:
            cursor = connection.cursor()
            cursor.execute(sql_query)
            results = cursor.fetchall()
            return results
    except sqlite3.Error as e:
        raise Exception(f"Database error: {e}")

# Step 2: Create a chat completion request
@retry(wait=wait_random_exponential(min=1, max=40), stop=stop_after_attempt(3))
def create_chat_completion_request(user_query: str):
    try:
        # Step 2.1: Include the database schema in the system prompt
        system_prompt = f"""
        You are a helpful assistant that queries a SQLite database to retrieve real estate information.
        The database schema is as follows:
        {database_schema}
        Always generate valid SQL queries based on this schema.
        """

        # Step 2.2: Send the initial chat completion request
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_query}
            ],
            tools=tools,
            tool_choice="auto"
        )

        # Step 2.3: Check if a function call is required
        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls

        if tool_calls:
            # Step 2.4: Handle function calling
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                if function_name == "query_database":
                    # Extract the SQL query from the function arguments
                    function_args = json.loads(tool_call.function.arguments)
                    sql_query = function_args["sql_query"]

                    # Execute the SQL query
                    print(f"Executing SQL query: {sql_query}")
                    query_results = query_database(sql_query)

                    # Step 2.5: Send the query results back to OpenAI
                    response = client.chat.completions.create(
                        model=MODEL,
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_query},
                            response_message,
                            {
                                "role": "tool",
                                "content": str(query_results),
                                "tool_call_id": tool_call.id
                            }
                        ]
                    )

                    # Step 2.6: Display the final response
                    print("Final response from OpenAI:")
                    print(response.choices[0].message.content)
        else:
            # Step 2.7: If no function call is required, display the response
            print("Response from OpenAI:")
            print(response_message.content)

    except Exception as e:
        print(f"Error: {e}")

# Step 3: Main execution
if __name__ == "__main__":
    print("Database schema:")
    print(database_schema)

    print("\nUser message:")
    print(USER_MESSAGE)

    print("\nProcessing the user query...")
    create_chat_completion_request(USER_MESSAGE)