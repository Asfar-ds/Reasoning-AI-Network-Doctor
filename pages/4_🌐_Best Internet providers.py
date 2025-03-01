import streamlit as st
from langchain import LLMChain, PromptTemplate
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
groq_api = os.getenv('GROQ_API_KEY')
os.environ['GROQ_API_KEY'] = groq_api  # Set the environment variable

# Set up the Streamlit page configuration
st.set_page_config(page_title='Best Internet Provider', layout='wide')

# Custom CSS for styling
st.markdown("""
<style>
.recommendation-box {
    background-color: #f0f2f6;
    border-radius: 10px;
    padding: 15px;
    margin: 10px 0;
    border: 1px solid #e0e0e0;
}
</style>
""", unsafe_allow_html=True)

# Title and Description
st.title('🛜 Best Internet Provider based on Usage')
st.write('This AI-powered internet recommender will recommend the best Internet Service Provider based on your usage.')

# User input fields
st.subheader("⚡ Kindly provide your usage details")
mbs_needed = st.slider('Preferred Internet Speed (MBs)', 1, 300, 30)
ms = st.slider('Preferred MS (ping)', 20, 800, 60)
no_of_meters = st.slider('Average distance between device and modem (meters)', 1, 30, 5)
no_of_devices = st.slider('Number of Devices that could be connected to your network', 1, 50, 5)
usage_type = st.selectbox('Select Your Usage Type', ['Browsing', 'Freelancing', 'Gaming', "Surfing", 'Streaming', "Work", "Other"])
your_device_type = st.selectbox('Your Device Type', ["Laptop", "Mobile", "Smart TV", "Gaming Console"])
selected_country = st.text_input('Kindly Enter your Country name')
vpn = st.radio('Will you use VPN?', ['Yes', 'No', "Sometimes"])

# New input field for issues they are facing
current_issues = st.text_input('What issues are you facing with your current internet? (e.g., slow speed, frequent disconnections, high ping)')

# Groq model setup
llm = ChatGroq(model='llama-3.3-70b-versatile')

# Define the prompt template for the Groq model
prompt_template = PromptTemplate(
    input_variables=["mbs_needed", "ms", "no_of_meters", "no_of_devices", "usage_type", "your_device_type", "vpn", "selected_country", "current_issues"],
    template="""
    Based on the following user preferences and issues, recommend the best Internet Service Provider:
    - Preferred Internet Speed: {mbs_needed} MBs
    - Preferred MS (ping): {ms}
    - Average distance between device and modem: {no_of_meters} meters
    - Number of Devices: {no_of_devices}
    - Usage Type: {usage_type}
    - Device Type: {your_device_type}
    - VPN Usage: {vpn}
    - Country: {selected_country}
    - Current Issues: {current_issues}

    Just give the best ISP provider name according to the user's preferences and issues mentioned above. Also, provide a brief explanation of why it is the best fit and how it addresses the user's current issues.
    If the user has not mentioned their country name, ask them to mention it and do not provide an answer.
    """
)

# Create the LLMChain
chain = LLMChain(llm=llm, prompt=prompt_template)

# Button to generate recommendation
if st.button('Get Recommendation'):
    if not selected_country:
        st.warning("Please enter your country name to get a recommendation.")
    else:
        # Prepare the input data
        input_data = {
            "mbs_needed": mbs_needed,
            "ms": ms,
            "no_of_meters": no_of_meters,
            "no_of_devices": no_of_devices,
            "usage_type": usage_type,
            "your_device_type": your_device_type,
            "vpn": vpn,
            "selected_country": selected_country,
            "current_issues": current_issues
        }

        # Get the recommendation from the Groq model
        recommendation = chain.run(input_data)

        # Display the recommendation in Markdown format
        st.markdown('<div class="recommendation-box">', unsafe_allow_html=True)
        st.subheader("🎯 Recommended Internet Service Provider")
        st.markdown(f"""
        {recommendation}
        """)
        st.markdown('</div>', unsafe_allow_html=True)