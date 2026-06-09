import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")
api_key = os.getenv("AZURE_OPENAI_API_KEY")

if not endpoint or not deployment or not api_key:
    print("Missing .env values. Check your .env file.")
    sys.exit(1)

def read_terraform_files():
    current_folder = Path.cwd()
    tf_files = list(current_folder.glob("*.tf"))

    if not tf_files:
        return "No Terraform .tf files found in this current folder."

    content = ""

    for file in tf_files:
        content += f"\n\n--- FILE: {file.name} ---\n"
        content += file.read_text(encoding="utf-8", errors="ignore")

    return content

args = sys.argv[1:]

if not args:
    question = input("Ask your Terraform Copilot: ")
else:
    command = " ".join(args)

    if command.lower() == "review":
        terraform_code = read_terraform_files()
        question = (
            "Review these Terraform files like a beginner-friendly Azure Cloud Engineer. "
            "Explain what the code is doing, find mistakes, suggest improvements, and explain everything simply.\n\n"
            + terraform_code
        )
    elif command.lower() == "explain":
        terraform_code = read_terraform_files()
        question = (
            "Explain these Terraform files line by line in beginner language:\n\n"
            + terraform_code
        )
    else:
        question = command

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
                "You are Anson's beginner-friendly Azure Terraform Copilot. "
                "Explain slowly and clearly. Do not assume the user knows advanced words. "
                "Give practical fixes, commands, and examples."
            )
        },
        {
            "role": "user",
            "content": question
        }
    ],
)

print(response.choices[0].message.content)