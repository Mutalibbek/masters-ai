import os
import sqlite3
import json
import re
import streamlit as st
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv
from tenacity import retry, wait_random_exponential, stop_after_attempt
import freecurrencyapi
import openai

# Load environment variables
load_dotenv()
st.set_page_config(layout="wide")

# Constants
MODEL = "gpt-4"
# MODEL = "deepseek-chat"
DATABASE = os.getenv("MY_DATABASE")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
FREE_API_KEY = os.getenv("FREECURRENCYAPI_KEY")
SQL_REQUEST_START = "SELECT * FROM buildings_with_coordinates ORDER BY project_no ASC;"


# Initialize OpenAI client
openai.api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()


# Initialize OpenAI client for DeepSeek
# client = OpenAI(
#     api_key=DEEPSEEK_API_KEY,
#     base_url="https://api.deepseek.com/v1")

# Initialize FreeCurrencyAPI client
api_client = freecurrencyapi.Client(FREE_API_KEY)

# Database schema
database_schema = """
Table: buildings_with_coordinates
Columns:
- project_no: Integer - Unique identifier for each project.
- city: String - The city name written in English where the building is located.
- building_name: String - The name of the building or residential complex.
- price_per_sqm: String - The price per square meter, often in a range (e.g., "от 290 000 〒 за м²").
- min_price_per_sqm: Float - The minimum price per square meter.
- max_price_per_sqm: Float - The maximum price per square meter (if available).
- project_status: String - The current status of the project (e.g., "Сдан в эксплуатацию", "Строящийся").
- address: String - The full address of the building.
- company: String - The company or developer responsible for the project.
- accommodation_class: String - The class of accommodation (e.g., "комфорт", "элит", "бизнес").
- stories: String - The number of stories in the building.
- ceiling_height: String - The height of the ceilings (e.g., "2.8 м").
- building_type: String - The type of building construction (e.g., "кирпичный", "монолитный").
- decoration: String - The type of interior decoration (e.g., "черновая", "предчистовая").
- number_of_apartments: Integer - The total number of apartments in the building.
- kitchen: String - The type of kitchen (e.g., "полноценная", "студия").
- facade: String - The material or style of the building facade (e.g., "травертин", "фиброцементные панели").
- apartments_for_sale: Integer - The number of apartments available for sale.
- parking: String - The type of parking available (e.g., "надземный", "подземный").
- heating: String - The type of heating system (e.g., "центральное", "автономное").
- elevator: String - The type of elevator (e.g., "грузопассажирский", "пассажирский").
- nearby: String - Nearby amenities or landmarks (e.g., "школы, детские сады, поликлиники").
- inside: String - Amenities inside the building or complex (e.g., "детские игровые площадки, зоны отдыха").
- safety: String - Safety features (e.g., "видеонаблюдение", "круглосуточная охрана").
- description: String - A detailed description of the building or complex.
- source_website: String - The URL of the source website for the project.
- purchase_conditions: String - Conditions for purchasing (e.g., "Ипотека", "Рассрочка").
- payment_options: String - Payment options available (e.g., "Ипотека «7-20-25»", "Рассрочка от застройщика").
- location_id: Integer - A unique identifier for the location.
- price_float: Float - The price per square meter as a float.
- ceiling_height_float: Float - The ceiling height as a float.
- stories_float: Float - The number of stories as a float.
- full_address: String - The full address including city and street.
- latitude: Float - The latitude coordinate of the building.
- longitude: Float - The longitude coordinate of the building.
"""

# Currency schema
currency_schema = """
EUR:	Euro
USD:	US Dollar
JPY:	Japanese Yen
BGN:	Bulgarian Lev
CZK:	Czech Republic Koruna
DKK:	Danish Krone
GBP:	British Pound Sterling
HUF:	Hungarian Forint
PLN:	Polish Zloty
RON:	Romanian Leu
SEK:	Swedish Krona
CHF:	Swiss Franc
ISK:	Icelandic Króna
NOK:	Norwegian Krone
HRK:	Croatian Kuna
RUB:	Russian Ruble
TRY:	Turkish Lira
AUD:	Australian Dollar
BRL:	Brazilian Real
CAD:	Canadian Dollar
CNY:	Chinese Yuan
HKD:	Hong Kong Dollar
IDR:	Indonesian Rupiah
ILS:	Israeli New Sheqel
INR:	Indian Rupee
KRW:	South Korean Won
MXN:	Mexican Peso
MYR:	Malaysian Ringgit
NZD:	New Zealand Dollar
PHP:	Philippine Peso
SGD:	Singapore Dollar
THB:	Thai Baht
ZAR:	South African Rand
"""

tools = [
    {
        "type": "function",
        "function": {
            "name": "query_database",
            "description": "Query an SQLite database to retrieve real estate information.",
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
    },
    {
        "type": "function",
        "function": {
            "name": "convert_currency",
            "description": "Convert the price in the database into another currency.",
            "parameters": {
                "type": "object",
                "properties": {
                    "amount": {
                        "type": "number",
                        "description": "The amount to convert."
                    },
                    "base_currency": {
                        "type": "string",
                        "description": "The base currency code."
                    },
                    "target_currency": {
                        "type": "string",
                        "description": "The target currency code."
                    }
                },
                "required": ["amount", "base_currency", "target_currency"],
                "additionalProperties": False
            }
        }
    }
]


def get_data_as_dataframe_from_db(sql_query) -> pd.DataFrame:
    data = query_database(sql_query)
    headers = [
    "project_no", "city", "building_name", "price_per_sqm", "min_price_per_sqm", "max_price_per_sqm",
    "project_status", "address", "company", "accommodation_class", "stories", "ceiling_height",
    "building_type", "decoration", "number_of_apartments", "kitchen", "facade",
    "apartments_for_sale", "parking", "heating", "elevator", "nearby", "inside", "safety",
    "description", "source_website", "purchase_conditions", "payment_options", "location_id",
    "price_float", "ceiling_height_float", "stories_float", "full_address", "latitude", "longitude"
]
    return pd.DataFrame(data, columns=headers)

# Helper functions
def make_sqlquery_case_insensitive(sql_query: str) -> str:
    # Use regex to find text comparisons and add COLLATE NOCASE
    # Example: WHERE city = 'Almaty' -> WHERE city COLLATE NOCASE = 'Almaty'
    pattern = re.compile(r"(\b\w+\b\s*=\s*'[^']*')", re.IGNORECASE)
    modified_query = pattern.sub(r"\1 COLLATE NOCASE", sql_query)
    return modified_query

def get_exchange_rate(base_currency: str, target_currency: str) -> float:
    try:
        result = api_client.latest(base_currency=base_currency, currencies=[target_currency])
        return result['data'][target_currency]  # Extract exchange rate
    except Exception as e:
        print(f"Error fetching exchange rate: {e}")
        return None

# Agents
def query_database(sql_query: str):
    try:
        sql_query = make_sqlquery_case_insensitive(sql_query)

        with sqlite3.connect(DATABASE) as connection:
            cursor = connection.cursor()
            cursor.execute(sql_query)
            columns = [column[0] for column in cursor.description]
            results = [dict(zip(columns, row)) for row in cursor.fetchall()]

        # Store results in session state for dynamic updates
        st.session_state.df = pd.DataFrame(results, columns=columns)

        return results  # Returning the raw data if needed
    except sqlite3.Error as error:
        print(f"Database error: {error}")
        raise Exception(f"Database error: {error}")

def convert_currency(amount: float, base_currency: str, target_currency: str) -> float:
    rate = get_exchange_rate(base_currency, target_currency)
    if rate is not None:
        return amount * rate
    else:
        print("Conversion failed. Check exchange rate.")
        return None

# Function calling
def handle_function_call(tool_call):
    function_name = tool_call.function.name
    function_args = json.loads(tool_call.function.arguments)

    if function_name == "query_database":
        sql_query = function_args["sql_query"]
        return query_database(sql_query)
    elif function_name == "convert_currency":
        amount = function_args["amount"]
        base_currency = function_args["base_currency"]
        target_currency = function_args["target_currency"]
        return convert_currency(amount, base_currency, target_currency)
    else:
        print(f"Unknown function: {function_name}")
        raise ValueError(f"Unknown function: {function_name}")

# Chat completion request
@retry(wait=wait_random_exponential(min=1, max=40), stop=stop_after_attempt(3))
def create_chat_completion_request(user_message: str):
    try:
        # Step 4.1: Include the database schema in the system prompt
        system_prompt = f"""
        You are a helpful assistant that queries a SQLite database to retrieve real estate information.
        The database schema is as follows:
        {database_schema}
        Always generate only valid SQL queries based on this schema. 
        You can also convert currencies using these currency codes
        {currency_schema}. Always use and return only currency codes (e.g. USD, EUR)
        """

        # Step 4.2: Send the initial chat completion request
        gpt_response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            tools=tools,
            tool_choice="auto"
        )

        # Step 4.3: Check if a function call is required
        response_message = gpt_response.choices[0].message

        tool_calls = response_message.tool_calls

        if tool_calls:
            for tool_call in tool_calls:
                function_response = handle_function_call(tool_call)  # Execute the SQL modification

                return function_response  # Directly return the SQL result

    except Exception as e:
        print(f"Error in create_chat_completion_request: {e}")
        raise Exception(f"Error: {e}")

def main():
    left_side, right_side = st.columns([0.65, 0.30], gap="large", border=True)

    # Initialize DataFrame in session state
    if "df" not in st.session_state or st.session_state.df is None:
        st.session_state.df = pd.DataFrame(query_database(SQL_REQUEST_START))
    df = st.session_state.df

    # Left side - Data display (unchanged)
    with left_side:
        st.title("Real Estate Listings")
        if not df.empty:
            df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
            df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')
            clean_df = df.dropna(subset=['latitude', 'longitude'])
            st.dataframe(clean_df)
            st.map(clean_df[['latitude', 'longitude']])
        else:
            st.warning("No data found.")

    # Right side - Chat interface (modified)
    with right_side:
        st.title("Real Estate Chatbot 🏠")
        st.write("Ask me anything about real estate!")

        if "messages" not in st.session_state:
            st.session_state.messages = [
                {"role": "assistant", "content": "Hi, I am your real estate assistant. How can I help?"}
            ]

        # Display messages without data structures
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                # Filter out any list/table outputs
                if isinstance(message["content"], (list, pd.DataFrame)):
                    continue  # Skip rendering structured data
                st.markdown(message["content"])

        if user_query := st.chat_input("Ask a question..."):
            st.session_state.messages.append({"role": "user", "content": user_query})

            with st.chat_message("user"):
                st.markdown(user_query)

            with st.spinner("Thinking..."):
                try:
                    response = create_chat_completion_request(user_query)

                    # Always convert to natural language response
                    if isinstance(response, list):
                        response_text = f"I have found {len(response)} properties matching your query."
                    elif isinstance(response, pd.DataFrame):
                        response_text = f"Dataset updated with {len(response)} entries."
                    else:
                        response_text = str(response)

                    # Append only text to chat history
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": response_text
                    })

                    st.rerun()

                except Exception as e:
                    st.error(f"Error processing query: {e}")
                    print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
