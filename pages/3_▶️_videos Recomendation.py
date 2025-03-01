import streamlit as st
from googleapiclient.discovery import build
import os
from dotenv import load_dotenv

load_dotenv()
# API key
API_KEY = os.getenv('youtube_api_key')

# Function to search YouTube videos
def search_youtube_videos(query, max_results=5):
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    request = youtube.search().list(
        q=query,
        part='snippet',
        type='video',
        maxResults=max_results
    )
    response = request.execute()
    videos = []
    for item in response['items']:
        video_id = item['id']['videoId']
        video_title = item['snippet']['title']
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        videos.append((video_title, video_url))
    return videos

# Set Streamlit page config
st.set_page_config(page_title="YouTube Video Search", layout="wide")

# Custom CSS for styling
st.markdown("""
<style>
.video-card {
    background-color: #f5f5f5;
    border-radius: 10px;
    padding: 15px;
    margin: 10px 0;
    border: 1px solid #e0e0e0;
}
.video-card a {
    color: #1f77b4;
    text-decoration: none;
}
.video-card a:hover {
    text-decoration: underline;
}
</style>
""", unsafe_allow_html=True)

# Title and Description
st.title('🎥 YouTube Video Search')
st.subheader("Enter a search query to find relevant YouTube videos.")

# User input for search query
query = st.text_input("Enter your search query:", "How to fix packet loss")

# Number of results to display
max_results = st.slider("Number of videos to display:", 1, 10, 5)

# Search for videos when the user clicks the button
if st.button("Search"):
    st.write(f"Searching for: **{query}**")
    videos = search_youtube_videos(query, max_results=max_results)
    
    if videos:
        st.write(f"Here are {len(videos)} YouTube videos that might help:")
        for title, url in videos:
            st.markdown(f"""
            <div class="video-card">
                <a href="{url}" target="_blank">{title}</a>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.write("No relevant videos found.")
