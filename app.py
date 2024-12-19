import streamlit as st
from dotenv import load_dotenv 
import os 
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
import re  # use to take Video ID from All Type of Link

load_dotenv()  # Read .env file and load variables into environment
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))  # Retrieve the key from environment and pass the API Key

# Prompt for summarization
prompt = """You are Youtube video summarizer. You will be taking the transcript text and summarizing the entire video and providing the important Heading("The Video Heading") and Introduction("The whole introduction about the video"), Key Points, Notable Quotes, and Conclusion."""

# Function to extract video ID from YouTube link
def extract_video_id(youtube_link):
    # Regular expression to capture YouTube video ID from various formats
    pattern = r"(?:v=|\/)([a-zA-Z0-9_-]{11})"
    match = re.search(pattern, youtube_link)
    if match:
        return match.group(1)
    return None

# Function to extract transcript from YouTube
def extract_transcript_details(youtube_video_url):
    try:
        video_id = extract_video_id(youtube_video_url)
        if not video_id:
            raise ValueError("Invalid YouTube video URL. Could not extract video ID.")
        
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)  # Use this Video ID to access the YouTube Video, Use the YT's Caption for the content

        transcript = ""  # Separated content stored here
        for i in transcript_text:
            transcript += " " + i["text"]

        return transcript

    except Exception as e:
        raise e

# Function to generate summary using Google Gemini Pro
def generate_gemini_content(transcript_text):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt + transcript_text)
    return response.text


# Streamlit interface
st.title("YouTube Transcript")
youtube_link = st.text_input("Enter YouTube Video Link")

# if youtube_link:
#     video_id = extract_video_id(youtube_link)
#     if video_id:
#         st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_container_width=True)
#     else:
#         st.error("Invalid YouTube link. Could not extract video ID.")

# if st.button("Get Content"):
#     if youtube_link:
#         try:
#             transcript_text = extract_transcript_details(youtube_link)

#             if transcript_text:
#                 summary = generate_gemini_content(transcript_text)

#                 # Store the summary in a text file
#                 with open("video_content.txt", "w", encoding="utf-8") as file:
#                     file.write(summary)

#                 st.markdown("# Blog Content:")
                

                
#                 if youtube_link:
#                     video_id = extract_video_id(youtube_link)
#                     if video_id:
#                         st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_container_width=True)
#                     else:
#                         st.error("Invalid YouTube link. Could not extract video ID.")
                        
#                 # If possible, add the Image from Unsplash
#                 st.write(summary)
#                 st.success("Summary has been saved to 'video_content.txt'")
#         except Exception as e:
#             st.error(f"An error occurred: {e}")
#     else:
#         st.error("Please provide a valid YouTube link.")

if st.button("Get Content"):
    if youtube_link:
        try:
            transcript_text = extract_transcript_details(youtube_link)

            if transcript_text:
                summary = generate_gemini_content(transcript_text)

                # Store the summary in a text file
                with open("video_content.txt", "w", encoding="utf-8") as file:
                    file.write(summary)

                st.markdown("# Blog Content:")

                if youtube_link:
                    video_id = extract_video_id(youtube_link)
                    if video_id:
                        # Corrected image display line
                        st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)
                    else:
                        st.error("Invalid YouTube link. Could not extract video ID.")
                        
                # If possible, add the Image from Unsplash
                st.write(summary)
                st.success("Summary has been saved to 'video_content.txt'")
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.error("Please provide a valid YouTube link.")

