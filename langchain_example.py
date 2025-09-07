from langchain_aws import ChatBedrock


llm = ChatBedrock(model="us.amazon.nova-lite-v1:0")

messages = [
    ("user", "Write a short poem about the moon.")
]

for chunk in llm.stream(messages):
    print(chunk.text(), end="|")
