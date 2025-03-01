import streamlit as st
from PIL import Image
import requests
from io import BytesIO
# 
# Set Page Title and Layout
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
    .image-container {
        text-align: center;
        margin-top: 20px;
        margin-bottom: 20px;
    }
    .image-container img {
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    .footer {
        text-align: center;
        color: #666;
        font-size: 14px;
        margin-top: 40px;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="header">📡 AI Network Doctor - Intelligent Troubleshooting</div>', unsafe_allow_html=True)

# Add a relevant image after the title
st.markdown('<div class="image-container">', unsafe_allow_html=True)
image_url = "https://images.unsplash.com/photo-1564760290292-23341e4df6ec?q=80&w=1470&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"  # Network-related image
response = requests.get(image_url)
image = Image.open(BytesIO(response.content))
st.image(image, caption="Optimize Your Network with AI", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# Introduction
st.write("""
Welcome to **AI Network Doctor**, your **AI-powered assistant** for diagnosing and troubleshooting network issues! 🚀  

Are you tired of dealing with **slow internet**, **high ping**, or **random disconnections**? You're not alone! We’ve all been there, and it’s frustrating. But don’t worry—this tool is here to help.  

With **AI Network Doctor**, you can:  
- **Identify potential network issues** in real-time  
- Get **actionable tips** to fix your connection  
- **Optimize your internet performance** for streaming, gaming, or work  
- Support for **all devices**—whether you're on a laptop, phone, or smart TV  

Ready to take control of your network? Click on **"Diagnose My Network"** in the sidebar, and let’s get started! 🛠️  
""")

# Highlight Section
st.markdown('<div class="highlight">', unsafe_allow_html=True)
st.markdown("""
### 🚀 Why Choose AI Network Doctor?  
- **AI-Powered Insights**: Our advanced AI analyzes your network conditions and provides tailored recommendations.  
- **Real-Time Diagnostics**: Get instant feedback on your network health.  
- **User-Friendly**: No technical expertise required—just answer a few questions, and we’ll handle the rest.  
- **Free & Accessible**: No downloads or installations needed. Just open your browser and go!  
""")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")
st.markdown('<div class="footer">Made with ❤️ by <b>AI Network Doctor</b> | Powered by Streamlit & AI</div>', unsafe_allow_html=True)