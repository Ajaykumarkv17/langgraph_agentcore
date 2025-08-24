from langchain_aws import ChatBedrock

import os

from dotenv import load_dotenv

load_dotenv()

bedrock_api_key = os.getenv("AWS_BEARER_TOKEN_BEDROCK")
llm = ChatBedrock(model="us.amazon.nova-lite-v1:0",api_key=bedrock_api_key)

messages = [
    ("user", "Write a short poem about the moon.")
]

print(llm.invoke(messages))
