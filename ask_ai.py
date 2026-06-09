import os
import sys
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")
api_key = os.getenv("AZURE_OPENAI_API_KEY")

if not endpoint or not deployment or not api_key:
    print("Missing .env values. Check AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_DEPLOYMENT, and AZURE_OPENAI_API_KEY.")
    sys.exit(1)

question = " ".join(sys.argv[1:])

if not question:
    question = input("Ask your Terraform Copilot: ")

client = OpenAI(
    base_url=endpoint,
    api_key=api_key
)

response = client.chat.completions.create(
    model=deployment,
    messages=[
        {
            "role": "system",
            "content": (
                "You are a beginner-friendly Terraform and Azure Cloud Engineer assistant. "
                "Explain everything slowly, do not assume the user knows advanced terms, "
                "and give practical commands and examples."
            )
        },
        {
            "role": "user",
            "content": question
        }
    ],
)

print(response.choices[0].message.content)