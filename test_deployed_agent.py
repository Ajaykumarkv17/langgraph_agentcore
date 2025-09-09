
import boto3
import json
  
# Initialize the Bedrock AgentCore client
agent_core_client = boto3.client('bedrock-agentcore')

prompt = "I want to book an appointment with a cardiologist next Monday at 10 AM."
agent_arn = "arn:aws:bedrock-agentcore:us-east-1:992382390542:runtime/langgraph_hospital_assistant-A2KCnpGUQn"
# session_id = "test-session-001"

# Prepare the payload
payload = json.dumps({"prompt": prompt}).encode()
  
# Invoke the agent
response = agent_core_client.invoke_agent_runtime(
    agentRuntimeArn=agent_arn,
    payload=payload
)
  
  
# Process and print the response
if "text/event-stream" in response.get("contentType", ""):
  
    # Handle streaming response
    content = []
    for line in response["response"].iter_lines(chunk_size=10):
        if line:
            line = line.decode("utf-8")
            if line.startswith("data: "):
                line = line[6:]
                print(line)
                content.append(line)
    print("\nComplete response:", "\n".join(content))

elif response.get("contentType") == "application/json":
    # Handle standard JSON response
    content = []
    for chunk in response.get("response", []):
        content.append(chunk.decode('utf-8'))
    print(json.loads(''.join(content)))
  
else:
    # Print raw response for other content types
    print(response)
