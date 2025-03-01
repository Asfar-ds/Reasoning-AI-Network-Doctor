from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
groq_api = os.getenv('GROQ_API_KEY')
os.environ['GROQ_API_KEY'] = groq_api  # Set the environment variable

# Setting up session states
if 'predicted_issue_ofGroq' not in st.session_state:
    st.session_state['predicted_issue_ofGroq'] = None

# Set Streamlit page config
st.set_page_config(page_title="AI Network Doctor", layout="wide", page_icon="📡")

# Custom CSS for styling
st.markdown("""
<style>
    .header {
        font-size: 40px;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 20px;
    }
    .subheader {
        font-size: 24px;
        font-weight: bold;
        color: #2ca02c;
        margin-top: 20px;
        margin-bottom: 10px;
    }
    .highlight {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 20px;
    }
    .button {
        background-color: #1f77b4;
        color: white;
        padding: 10px 20px;
        border-radius: 5px;
        text-align: center;
        font-size: 16px;
        font-weight: bold;
        cursor: pointer;
    }
    .button:hover {
        background-color: #1565c0;
    }
    .issue-list {
        font-size: 16px;
        color: #333;
        margin-bottom: 20px;
    }
    .footer {
        text-align: center;
        color: #666;
        font-size: 14px;
        margin-top: 40px;
    }
</style>
""", unsafe_allow_html=True)

# Title and Description
st.markdown('<div class="header">📡 AI Network Doctor - Intelligent Troubleshooting</div>', unsafe_allow_html=True)
st.write("""
This **AI-powered network troubleshooter** simulates **real-time diagnostics** based on your network conditions.  
Whether you're experiencing **slow internet**, **high ping**, or **connectivity issues**, this tool will help you identify and fix the problem. 🚀  
""")

# Collect User Inputs
st.markdown('<div class="subheader">🌍 Provide Your Network Details</div>', unsafe_allow_html=True)

# Input Fields
col1, col2 = st.columns(2)

with col1:
    # 1️⃣ Internet Speed (Mbps)
    internet_speed = st.slider("Select your Internet Speed (Mbps)", 1, 500, 50, help="Your current internet speed in Mbps.")

    # 2️⃣ Ping (ms)
    ping = st.slider("Select your Average Ping (ms)", 1, 500, 30, help="Your average ping in milliseconds.")

    # 3️⃣ WiFi Signal Strength
    wifi_strength = st.selectbox("Select your WiFi Strength", ["Excellent", "Good", "Weak", "Very Weak"], help="The strength of your WiFi signal.")

    # 4️⃣ Device Type
    device_type = st.selectbox("Select your Device", ["Laptop", "Mobile", "Smart TV", "Gaming Console"], help="The type of device you're using.")

with col2:
    # 5️⃣ Usage Type
    usage_type = st.selectbox("What are you using the network for?", ["Browsing", "Streaming", "Gaming", "Work"], help="The primary use of your network.")

    # 6️⃣ Network Type
    network_type = st.selectbox("What type of network are you using?", ["WiFi", "Ethernet", "Mobile Data", "Satellite"], help="The type of network connection.")

    # 7️⃣ Router Distance (meters)
    router_distance = st.slider("How far is your device from the router? (meters)", 0, 50, 5, help="The distance between your device and the router.")

    # 8️⃣ Connected Devices Count
    connected_devices = st.slider("How many devices are connected to the network?", 1, 50, 5, help="The number of devices connected to your network.")

# 9️⃣ VPN Usage
vpn_usage = st.radio("Are you using a VPN?", ["Yes", "No"], help="Whether you're using a VPN or not.")

# Possible Issues
potential_issues = [
    "🚨 Packet loss detected", 
    "❌ Router unreachable", 
    "🔄 DNS failure", 
    "⚠️ IP conflict detected", 
    "🛑 Firewall blocking traffic", 
    "🚦 ISP throttling suspected", 
    "🔧 DHCP server failure",
    "🔴 High CPU usage on network switch",        
    "📡 Modem firmware outdated",             
    "🔋 Low power on wireless access point",  
    "⚡ Asymmetric routing causing packet drops",  
    "🔀 BGP route flapping detected",             
    "🛠️ MTU mismatch causing fragmentation",      
    "📊 QoS misconfiguration affecting traffic",  
    "🌍 Dual-stack IPv4/IPv6 misconfiguration",   
    "🔐 SSL/TLS handshake failure",               
    "📡 STP loop causing broadcast storms",       
    "🔄 OSPF neighbor adjacency failure"          
]

# **Predict an Issue Based on Inputs**
if st.button("🔍 Diagnose My Network", key="diagnose_button"):
    st.markdown('<div class="subheader">🛠️ Diagnosing Your Network...</div>', unsafe_allow_html=True)
    issue_prompt = PromptTemplate.from_template(
        'You are an AI assistant and predict network-related issues based on the given details.\n'
        "I am experiencing issues with my internet connection. Here are the details:\n"
        "Internet Speed: {internet_speed} Mbps\n"
        "Ping: {ping} ms\n"
        "WiFi Strength: {wifi_strength}\n"
        "Device Type: {device_type}\n"
        "Usage: {usage}\n"
        "Network Type: {network_type}\n"
        "Router Distance: {router_distance} meters\n"
        "Connected Devices: {connected_devices}\n"
        "VPN Usage: {vpn_usage}\n\n"
        "These are the possible issues. You must predict only from these issues: {Issues}\n"
        "Remember, you are restricted to **only these issues**.\n"
        "Provide exactly **2 potential issues**.\n"
        "If the issue name is simple, make it complex so that a layman cannot easily understand it."
        "Do not give any information with issues. Only give their name. only name. not anything else"
    )

    Predict_issue_prompt = issue_prompt.invoke({
        'internet_speed': internet_speed,
        'ping': ping,
        'wifi_strength': wifi_strength,
        'device_type': device_type,
        'usage': usage_type,
        'network_type': network_type,
        'router_distance': router_distance,
        'connected_devices': connected_devices,
        'vpn_usage': vpn_usage,
        'Issues': potential_issues
    })

    model_groq = ChatGroq(model='gemma2-9b-it')
    predicted_issue = model_groq.invoke(Predict_issue_prompt)
    st.session_state['predicted_issue_ofGroq'] = predicted_issue.content
    st.markdown('<div class="subheader">🎯 Predicted Issues:</div>', unsafe_allow_html=True)
    st.write(st.session_state['predicted_issue_ofGroq'])

# **Ask AI to Help Solve This Problem**
if st.session_state['predicted_issue_ofGroq']:
    if st.button("🤖 Ask AI to Help Solve This Problem", key="solve_button"):
        prompt_template = PromptTemplate.from_template(
            "You are a Ai assistant who give suggestion to fix the network issues:\n"
            "the user will provide you the issue and you have to suggest him the best ways to solve the issue. do not ask him to provide more information. Give detailed answer\n"
            "the issue are following: {predicted_issues}"
            "You only have these predicted issues. Only reply based on these"
        )

        ai_model_input = prompt_template.invoke({
            'predicted_issues': st.session_state.predicted_issue_ofGroq
        })

        solver_groq = ChatGroq(model='gemma2-9b-it')         
        Solve_issue = solver_groq.invoke(ai_model_input).content
        st.markdown('<div class="subheader">🛠️ Solution:</div>', unsafe_allow_html=True)
        st.write(Solve_issue)

# Footer
st.markdown("---")
st.markdown('<div class="footer">Made with ❤️ by <b>AI Network Doctor</b> | Powered by Streamlit & AI</div>', unsafe_allow_html=True)