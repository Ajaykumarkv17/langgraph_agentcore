from langgraph_hospital_assistant import graph

def test_hospital_assistant():
    system_prompt = """
    You are MediCare Hospital Assistant, a helpful and professional AI assistant for MediCare General Hospital.
    
    Your capabilities include:
    - Booking appointments with doctors
    - Listing doctors and their specializations
    - Checking doctor availability
    - Providing hospital information and services
    - Searching existing appointments
    - Giving health tips and advice
    - General medical information search
    
    Always be polite, professional, and helpful.
    """
    
    print("🏥 MediCare Hospital Assistant")
    print("Type 'quit' to exit\n")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() in ['quit', 'exit', 'bye']:
            print("Thank you for using MediCare Hospital Assistant!")
            break
            
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ]
        
        try:
            result = graph.invoke({"messages": messages})
            response = result['messages'][-1].content
            print(f"Assistant: {response}\n")
        except Exception as e:
            print(f"Error: {e}\n")

if __name__ == "__main__":
    test_hospital_assistant()