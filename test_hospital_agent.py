import requests
import json
import time

def test_hospital_agent(prompt):
    url = "http://127.0.0.1:8080/invocations"
    payload = {"prompt": prompt}
    
    print(f"\n🔵 Query: {prompt}")
    print("=" * 80)
    
    response = requests.post(url, json=payload)
    
    if response.status_code == 200:
        result = response.json()
        print(result['result'])
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
    
    print("=" * 80)
    time.sleep(1)

def run_comprehensive_test():
    print("🏥 MEDICARE HOSPITAL ASSISTANT - COMPREHENSIVE TEST")
    print("=" * 80)
    
    # Test cases covering all features
    test_cases = [
        # "Hello! What services do you provide?",
        # "Can you list all available doctors?",
        # "Show me cardiologists only",
        "What are the hospital departments?",
        # "Check availability of Dr. Sarah Johnson",
        # "I want to book an appointment with Dr. Michael Chen for John Smith on 2024-02-15 at 10:00 AM for headache consultation",
        # "What services does the hospital offer?",
        # "Give me hospital contact information",
        # "Search appointments for John Smith",
        # "Give me health tips for diabetes",
        # "What are general health tips?",
        # "Search for latest treatments for hypertension online"
    ]
    
    for test_case in test_cases:
        test_hospital_agent(test_case)
    
    # print("\n✅ Comprehensive test completed!")
    # print("\n📋 Available Commands:")
    # print("• List doctors: 'Show me all doctors' or 'List cardiologists'")
    # print("• Check availability: 'Is Dr. Sarah Johnson available?'")
    # print("• Book appointment: 'Book appointment with Dr. Chen for [name] on [date] at [time]'")
    # print("• Hospital info: 'What's the hospital address?'")
    # print("• Services: 'What services do you offer?'")
    # print("• Health tips: 'Give me health tips for diabetes'")
    # print("• Search appointments: 'Find appointments for [patient name]'")

if __name__ == "__main__":
    run_comprehensive_test()