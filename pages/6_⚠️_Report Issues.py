import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
from folium.plugins import HeatMap
from geopy.geocoders import Nominatim

# Set up the Streamlit page configuration
st.set_page_config(page_title='Community Asset Mapping', layout='wide')

# Title and Description
st.title('🌍 Community Asset Mapping')
st.write('Report and view local network issues to help improve connectivity in your area.')

# Initialize session state for storing reported issues
if 'reported_issues' not in st.session_state:
    st.session_state.reported_issues = pd.DataFrame(columns=['Latitude', 'Longitude', 'Issue', 'Description', 'User'])

# Function to add a new issue
def add_issue(lat, lon, issue, description, user):
    new_issue = pd.DataFrame({
        'Latitude': [lat],
        'Longitude': [lon],
        'Issue': [issue],
        'Description': [description],
        'User': [user]
    })
    st.session_state.reported_issues = pd.concat([st.session_state.reported_issues, new_issue], ignore_index=True)

# Function to geocode an address
def geocode_address(address):
    geolocator = Nominatim(user_agent="community_asset_mapping")
    location = geolocator.geocode(address)
    if location:
        return location.latitude, location.longitude
    else:
        return None, None

# User input for reporting issues
st.subheader('📝 Report a Network Issue')
col1, col2 = st.columns(2)

with col1:
    address = st.text_input('Enter Address (e.g., New Delhi, India)', help="Enter the address of the issue location.")
    issue = st.selectbox('Select Issue Type', ['Slow Speed', 'Frequent Disconnections', 'High Latency', 'No Connectivity', 'Other'])
    description = st.text_area('Describe the Issue')

with col2:
    user = st.text_input('Your Name (Optional)', help="Enter your name to track your reported issues.")

if st.button('Report Issue'):
    if address:
        lat, lon = geocode_address(address)
        if lat and lon:
            add_issue(lat, lon, issue, description, user)
            st.success('Issue reported successfully!')
        else:
            st.error('Could not find the address. Please try again.')
    else:
        st.warning('Please enter a valid address.')

# Display the map with reported issues
st.subheader('🗺️ Reported Network Issues')
if not st.session_state.reported_issues.empty:
    # Create a Folium map centered at the mean of reported issues
    m = folium.Map(location=[st.session_state.reported_issues['Latitude'].mean(), 
                             st.session_state.reported_issues['Longitude'].mean()], 
                   zoom_start=10)

    # Add markers for each reported issue
    for index, row in st.session_state.reported_issues.iterrows():
        folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            popup=f"Issue: {row['Issue']}<br>Description: {row['Description']}<br>Reported by: {row['User']}",
            icon=folium.Icon(color='red', icon='exclamation-circle')
        ).add_to(m)

    # Add a heatmap for issue density
    heat_data = [[row['Latitude'], row['Longitude']] for index, row in st.session_state.reported_issues.iterrows()]
    HeatMap(heat_data).add_to(m)

    # Display the map
    folium_static(m)
else:
    # Default map location (e.g., New Delhi, India)
    m = folium.Map(location=[28.6139, 77.2090], zoom_start=10)
    folium_static(m)
    st.write('No issues reported yet. Be the first to report an issue!')

# Filters for reported issues
st.subheader('🔍 Filter Reported Issues')
issue_filter = st.multiselect('Filter by Issue Type', st.session_state.reported_issues['Issue'].unique())
user_filter = st.multiselect('Filter by User', st.session_state.reported_issues['User'].unique())

# Apply filters
filtered_issues = st.session_state.reported_issues
if issue_filter:
    filtered_issues = filtered_issues[filtered_issues['Issue'].isin(issue_filter)]
if user_filter:
    filtered_issues = filtered_issues[filtered_issues['User'].isin(user_filter)]

# Display the filtered table of reported issues
st.subheader('📋 List of Reported Issues')
st.dataframe(filtered_issues)

# Export reported issues as CSV
st.subheader('📤 Export Data')
if st.button('Export as CSV'):
    csv = filtered_issues.to_csv(index=False)
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name='reported_issues.csv',
        mime='text/csv'
    )   