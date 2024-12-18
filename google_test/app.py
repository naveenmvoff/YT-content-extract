# import streamlit as st
# from dotenv import load_dotenv

# load_dotenv()  # load all the environment variables
# import os
# import google.generativeai as genai

# from youtube_transcript_api import YouTubeTranscriptApi

# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# # Prompt for summarization
# prompt = """You are Youtube video summarizer. You will be taking the transcript text and summarizing the entire video and providing the important Heading("The Video Heading") and Introduction("The hole introduction about the video"), Key Points, Notable Quotes, and Conclusion. When generating you only give this ** and * to the Topic Titles only(Required)"""

# # Function to extract transcript from YouTube
# def extract_transcript_details(youtube_video_url):
#     try:
#         video_id = youtube_video_url.split("=")[1]
#         transcript_text = YouTubeTranscriptApi.get_transcript(video_id)

#         transcript = ""
#         for i in transcript_text:
#             transcript += " " + i["text"]

#         return transcript

#     except Exception as e:
#         raise e

# # Function to generate summary using Google Gemini Pro
# def generate_gemini_content(transcript_text):
#     model = genai.GenerativeModel("gemini-pro")
#     response = model.generate_content(prompt + transcript_text)
#     return response.text

# # Streamlit interface
# st.title("YouTube Transcript")
# youtube_link = st.text_input("Enter YouTube Video Link")

# if youtube_link:
#     video_id = youtube_link.split("=")[1]
#     st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

# if st.button("Get Detailed Notes"):
#     transcript_text = extract_transcript_details(youtube_link)

#     if transcript_text:
#         summary = generate_gemini_content(transcript_text)

#         # Store the summary in a text file
#         with open("video_content.txt", "w", encoding="utf-8") as file:
#             file.write(summary)

#         st.markdown("# Detailed Notes:")
#         st.write(summary)
#         st.success("Summary has been saved to 'video_content.txt'")


import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
import subprocess

load_dotenv()  # Load environment variables
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Prompt for summarization
# prompt = """You are Youtube video summarizer. You will be taking the transcript text and summarizing the entire video and providing the important Heading("The Video Heading") and Introduction("The whole introduction about the video"), Key Points, Notable Quotes, and Conclusion. When generating you only give this ** and * to the Topic Titles only(Required)(Like: **Introduction: In this video, we'll delve into the and next **Key Points: Definition of PaLM: PaLM (Patsgghdk) I need only in this format(Apart from this please Don't add anything like ** * *** * and other))"""
prompt = """You are Youtube video summarizer. You will be taking the transcript text and summarizing the entire video and providing the important Heading("The Video Heading", That should be only contain "**Heading", not like "**Heading**", "***Heading***") and Introduction("The whole introduction about the video", That should be only contain "**introduction", not like "**introduction**", "***introduction***") and Key Points (That should be only contain "**Key Points", not like "**Key Points**", "***Key Points***") and Notable Quotes (That should be only contain "**Notable Quotes", not like "**Notable Quotes**", "***Notable Quotes***") and Conclusion(That should be only contain "**Conclusion", not like "**Conclusion**", "***Conclusion***"),  Note(Required): Apart from mention format **Word, Don't use any other formate in any other lines"""

# Function to extract transcript from YouTube
def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("=")[1]
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)

        transcript = ""
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

# Function to run the http-server command
def run_http_server():
    try:
        # Run http-server command in terminal
        subprocess.run(["npx", "http-server", "."], check=True)
        st.success("Server started successfully!")
    except subprocess.CalledProcessError as e:
        st.error(f"Error starting server: {e}")

# Streamlit interface
st.title("YouTube Transcript")
youtube_link = st.text_input("Enter YouTube Video Link")

if youtube_link:
    video_id = youtube_link.split("=")[1]
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

if st.button("Get Detailed Notes"):
    transcript_text = extract_transcript_details(youtube_link)

    if transcript_text:
        summary = generate_gemini_content(transcript_text)

        # Store the summary in a text file
        with open("video_content.txt", "w", encoding="utf-8") as file:
            file.write(summary)

        st.markdown("# Detailed Notes:")
        st.write(summary)
        st.success("Summary has been saved to 'video_content.txt'")

# Add button to run the http-server command
if st.button("Start HTTP Server"):
    run_http_server()
