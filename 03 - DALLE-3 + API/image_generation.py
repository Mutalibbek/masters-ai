import openai
from dotenv import load_dotenv
import os

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

client = openai.OpenAI()
user_prompt = input("What image would you like to generate?")

response = client.images.generate(
  model="dall-e-3",
  prompt=user_prompt,
  n=1,
  size="1024x1024"
)

image_url = response.data[0].url

if __name__ == "__main__":
    print(f"Here is the link to the image: {image_url}")
