import openai
from dotenv import load_dotenv
import os

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def read_text_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()

def generate_text_from_openai(file_contents):
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Write a blog post based on the transcript of an online lecture on AI."},
        {"role": "user", "content": f"Here is the full transcript:\n{file_contents}"}
    ]

    client = openai.OpenAI()
    completion = client.chat.completions.create(
        model="gpt-4o",
        temperature=1,
        max_completion_tokens=16000,
        messages=messages
    )

    return completion.choices[0].message.content


if __name__ == "__main__":
    text_file_path = "Lecture transcript.txt"

    text_content = read_text_file(text_file_path)

    result = generate_text_from_openai(text_content)

    print("\nHere is a generated text:\n")
    print(result)
