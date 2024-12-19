import openai
from dotenv import load_dotenv
import os

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

client = openai.OpenAI()
user_prompt = input("What kind of image would you like to generate?")

styles = [
    "photorealistic",
    "watercolor painting",
    "pencil sketch",
    "oil painting",
    "cartoon",
    "digital art",
    "pixel art",
    "surrealism",
    "abstract"
]

image_urls = []
for style in styles:
    response = client.images.generate(
      model="dall-e-3",
      prompt=f"{user_prompt} in {style} style",
      n=1,
      size="1024x1024"
    )
    image_urls.append(response.data[0].url)

if __name__ == "__main__":
    print("Here are the links to the generated images in different styles:")
    for i, url in enumerate(image_urls, start=1):
        print(f"Image {i} in {styles[i - 1]} style: {url}")
