import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
groq_api = os.getenv('GROQ_API_KEY')
os.environ['GROQ_API_KEY'] = groq_api  # Set the environment variable

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display header only once at the start
if "hide_header" not in st.session_state:
    st.session_state.hide_header = False

if not st.session_state.hide_header:
    st.header('📡 Chat with Reasoning AI Network Doctor - Intelligent Troubleshooting')

# Initialize ChatGroq model
chat_model = ChatGroq(
    model='deepseek-r1-distill-llama-70b',
    temperature=0.5,
    top_p=0.5
)

# Define prompt template
prompts = PromptTemplate.from_template(
    "You are an AI Network Troubleshooting Assistant, specializing in diagnosing and resolving network-related issues. "
    "Your primary goal is to give detialed answr of the user queries "
    "Follow these guidelines:\n\n"
    
    "- If the user greets you (e.g., 'hi', 'hello', 'hey'), respond politely and professionally before asking how you can assist with a network issue.\n"
    "- If the user describes a network issue, provide a **concise troubleshooting guide** (3-5 sentences max), including possible causes and steps.\n"
    "- Do **not** ask for additional details—assume the user wants direct solutions.\n"
    "- Keep responses **short, professional, and easy to understand**.\n"
    "- If you need to 'think' before answering, summarize your thought process in **one short sentence** inside `<think>` tags.\n\n"

    "User's message: {question}"
    'Give longest possible answer. Your answer should be very very long'
)

# Custom CSS for the "thinking" box
st.markdown("""
<style>
.thinking-box {
    background-color: #2d2d2d;
    border-radius: 10px;
    padding: 10px;
    margin: 10px 0;
    border: 1px solid #444;
    font-family: monospace;
    color: #f0f0f0;
}
</style>
""", unsafe_allow_html=True)

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Get user input
user_input = st.chat_input("e.g. I am Facing High Ping ")

if user_input:
    # Hide the header after the first question
    st.session_state.hide_header = True

    # Append user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate AI response
    model_prompt = prompts.invoke({'question': user_input})
    model = chat_model.invoke(model_prompt)
    answer = model.content

    # Extract "thinking" part if present
    thinking_text = None
    final_answer = answer
    if "<think>" in answer and "</think>" in answer:
        thinking_text = answer.split("<think>")[1].split("</think>")[0].strip()
        final_answer = answer.split("</think>")[-1].strip()  # Remove thinking part

    # Display AI "thinking" box
    if thinking_text:
        st.markdown(f'<div class="thinking-box"><strong>🤔 Thinking:</strong> {thinking_text}</div>', unsafe_allow_html=True)

    # Display AI response
    with st.chat_message("assistant"):
        st.markdown(final_answer)

    # Append AI response to chat history
    st.session_state.messages.append({"role": "assistant", "content": final_answer})
