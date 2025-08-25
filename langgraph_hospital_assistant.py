from typing import Annotated, List, Dict, Any
from langchain.chat_models import init_chat_model
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.tools import tool
import os
import json
from datetime import datetime, timedelta
import random

from dotenv import load_dotenv

load_dotenv()


HOSPITAL_DATA = {
    "doctors": [
        {"id": 1, "name": "Dr. Sarah Johnson", "specialty": "Cardiology", "experience": 15, "rating": 4.8, "available_days": ["Monday", "Wednesday", "Friday"], "consultation_fee": 200},
        {"id": 2, "name": "Dr. Michael Chen", "specialty": "Neurology", "experience": 12, "rating": 4.9, "available_days": ["Tuesday", "Thursday", "Saturday"], "consultation_fee": 250},
        {"id": 3, "name": "Dr. Emily Rodriguez", "specialty": "Pediatrics", "experience": 8, "rating": 4.7, "available_days": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "consultation_fee": 150},
        {"id": 4, "name": "Dr. James Wilson", "specialty": "Orthopedics", "experience": 20, "rating": 4.6, "available_days": ["Monday", "Wednesday", "Friday", "Saturday"], "consultation_fee": 180},
        {"id": 5, "name": "Dr. Lisa Thompson", "specialty": "Dermatology", "experience": 10, "rating": 4.8, "available_days": ["Tuesday", "Thursday", "Friday"], "consultation_fee": 160},
        {"id": 6, "name": "Dr. Robert Kumar", "specialty": "General Medicine", "experience": 18, "rating": 4.5, "available_days": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"], "consultation_fee": 120}
    ],
    "departments": ["Cardiology", "Neurology", "Pediatrics", "Orthopedics", "Dermatology", "General Medicine", "Emergency", "Radiology", "Laboratory"],
    "services": ["Blood Test", "X-Ray", "MRI", "CT Scan", "ECG", "Ultrasound", "Vaccination", "Health Checkup"],
    "appointments": [],
    "hospital_info": {
        "name": "MediCare General Hospital",
        "address": "123 Health Street, Medical District, City 12345",
        "phone": "+1-555-HOSPITAL",
        "emergency": "+1-555-EMERGENCY",
        "hours": "24/7 Emergency | OPD: 8:00 AM - 8:00 PM"
    }
}

bedrock_api_key = os.getenv("AWS_BEARER_TOKEN_BEDROCK")
llm = init_chat_model(
    "us.amazon.nova-lite-v1:0",
    model_provider="bedrock",
    api_key=bedrock_api_key
)

# Hospital Tools
@tool
def list_doctors(specialty: str = None) -> str:
    """List all doctors or filter by specialty. Use specialty parameter to filter (e.g., 'Cardiology', 'Neurology')."""
    doctors = HOSPITAL_DATA["doctors"]
    if specialty:
        doctors = [d for d in doctors if d["specialty"].lower() == specialty.lower()]
    
    result = "Available Doctors:\n"
    for doc in doctors:
        result += f"• Dr. {doc['name']} - {doc['specialty']} | {doc['experience']} years exp | Rating: {doc['rating']}/5 | Fee: ${doc['consultation_fee']}\n"
    return result

@tool
def check_doctor_availability(doctor_name: str) -> str:
    """Check availability of a specific doctor by name."""
    doctor = next((d for d in HOSPITAL_DATA["doctors"] if doctor_name.lower() in d["name"].lower()), None)
    if not doctor:
        return f"Doctor {doctor_name} not found."
    
    return f"Dr. {doctor['name']} ({doctor['specialty']}) is available on: {', '.join(doctor['available_days'])}\nConsultation Fee: ${doctor['consultation_fee']}"

@tool
def book_appointment(doctor_name: str, patient_name: str, date: str, time: str, reason: str = "General consultation") -> str:
    """Book an appointment with a doctor. Format date as YYYY-MM-DD and time as HH:MM."""
    doctor = next((d for d in HOSPITAL_DATA["doctors"] if doctor_name.lower() in d["name"].lower()), None)
    if not doctor:
        return f"Doctor {doctor_name} not found."
    
    appointment_id = f"APT{random.randint(1000, 9999)}"
    appointment = {
        "id": appointment_id,
        "doctor": doctor["name"],
        "patient": patient_name,
        "date": date,
        "time": time,
        "reason": reason,
        "status": "Confirmed",
        "fee": doctor["consultation_fee"]
    }
    
    HOSPITAL_DATA["appointments"].append(appointment)
    return f"✅ Appointment booked successfully!\nAppointment ID: {appointment_id}\nDoctor: {doctor['name']}\nDate: {date} at {time}\nFee: ${doctor['consultation_fee']}"

@tool
def list_departments() -> str:
    """List all hospital departments."""
    return "Hospital Departments:\n" + "\n".join([f"• {dept}" for dept in HOSPITAL_DATA["departments"]])

@tool
def list_services() -> str:
    """List all hospital services available."""
    return "Hospital Services:\n" + "\n".join([f"• {service}" for service in HOSPITAL_DATA["services"]])

@tool
def get_hospital_info() -> str:
    """Get general hospital information including contact details and hours."""
    info = HOSPITAL_DATA["hospital_info"]
    return f"🏥 {info['name']}\n📍 Address: {info['address']}\n📞 Phone: {info['phone']}\n🚨 Emergency: {info['emergency']}\n🕒 Hours: {info['hours']}"

@tool
def search_appointments(patient_name: str = None) -> str:
    """Search for appointments by patient name."""
    appointments = HOSPITAL_DATA["appointments"]
    if patient_name:
        appointments = [a for a in appointments if patient_name.lower() in a["patient"].lower()]
    
    if not appointments:
        return "No appointments found."
    
    result = "Appointments:\n"
    for apt in appointments:
        result += f"• ID: {apt['id']} | {apt['patient']} with {apt['doctor']} | {apt['date']} at {apt['time']} | Status: {apt['status']}\n"
    return result

@tool
def get_health_tips(condition: str = None) -> str:
    """Get general health tips or tips for specific conditions."""
    tips = {
        "general": ["Drink 8 glasses of water daily", "Exercise for 30 minutes daily", "Get 7-8 hours of sleep", "Eat 5 servings of fruits and vegetables"],
        "diabetes": ["Monitor blood sugar regularly", "Follow a balanced diet", "Take medications as prescribed", "Exercise regularly"],
        "hypertension": ["Reduce salt intake", "Maintain healthy weight", "Limit alcohol", "Manage stress"],
        "heart": ["Avoid smoking", "Eat heart-healthy foods", "Exercise regularly", "Manage cholesterol"]
    }
    
    if condition and condition.lower() in tips:
        return f"Health Tips for {condition.title()}:\n" + "\n".join([f"• {tip}" for tip in tips[condition.lower()]])
    else:
        return "General Health Tips:\n" + "\n".join([f"• {tip}" for tip in tips["general"]])

from langchain_community.tools import DuckDuckGoSearchRun
search = DuckDuckGoSearchRun()

tools = [list_doctors, check_doctor_availability, book_appointment, list_departments, 
         list_services, get_hospital_info, search_appointments, get_health_tips, search]
llm_with_tools = llm.bind_tools(tools)

# Define state
class State(TypedDict):
    messages: Annotated[list, add_messages]

# Build the graph
graph_builder = StateGraph(State)

def chatbot(state: State):
    response = llm_with_tools.invoke(state["messages"])
    return {"messages": [response]}

graph_builder.add_node("chatbot", chatbot)
tool_node = ToolNode(tools=tools)
graph_builder.add_node("tools", tool_node)
graph_builder.add_conditional_edges("chatbot", tools_condition)
graph_builder.add_edge("tools", "chatbot")
graph_builder.add_edge(START, "chatbot")
graph = graph_builder.compile()

# Integrate with Bedrock AgentCore
from bedrock_agentcore.runtime import BedrockAgentCoreApp
app = BedrockAgentCoreApp()

@app.entrypoint
def agent_invocation(payload, context):
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
    
    Always be polite, professional, and helpful. When booking appointments, ensure you collect:
    - Patient name
    - Preferred doctor or specialty
    - Preferred date and time
    - Reason for visit
    
    If information is missing, politely ask for it. Always confirm appointment details before booking.
    """
    
    user_message = payload.get("prompt", "Hello, how can I help you today?")
    
    tmp_msg = {
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
    }
    
    tmp_output = graph.invoke(tmp_msg)
    return {"result": tmp_output['messages'][-1].content}

app.run()