# Real Estate Database Query Assistant

This Python script interacts with an SQLite database containing real estate information in Kazakhstan. 
It uses OpenAI's GPT-4 model to generate and execute SQL queries based on user input, retrieves the results, and displays them.

## Features

- **Database Interaction**: Connects to a SQLite database (`buildings_with_coordinates_2.db`) and executes SQL queries to retrieve real estate data.
- **OpenAI Integration**: Leverages OpenAI's GPT-4 model to generate SQL queries from natural language user input.
- **Function Calling**: Uses OpenAI's function calling feature to dynamically generate and execute SQL queries.
- **Error Handling**: Includes retry logic with exponential backoff to handle potential API errors.

## How It Works

1. **Environment Setup**: Loads environment variables using `dotenv` to securely manage the OpenAI API key.
2. **Database Schema**: Defines the schema of the SQLite database, including columns like `project_no`, `city`, `building_name`, `price_per_sqm`, and more.
3. **Function Definitions**:
   - `query_database(sql_query: str) -> list`: Executes a SQL query on the database and returns the results.
   - `create_chat_completion_request(user_query: str)`: Sends a chat completion request to OpenAI, handles function calling, and processes the results.
4. **Main Execution**:
   - Prints the database schema and the user's query.
   - Processes the user's query by sending it to OpenAI, which generates an appropriate SQL query.
   - Executes the SQL query and sends the results back to OpenAI for further processing.
   - Prints the final response from OpenAI, which includes the processed results.

## Usage

1. **Prerequisites**:
   - Python 3.x
   - OpenAI API key
   - SQLite database (`buildings_with_coordinates_2.db`)

2. **Install Dependencies**:
   ```bash
   pip install openai python-dotenv tenacity sqlite3