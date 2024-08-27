import streamlit as st
import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

# Configure the Google API key
GOOGLE_API_KEY = "AIzaSyBikV0v1ltCUIsVoLProMqJgx88fXNr6T0"
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

prompt = """"You are youTube video summarizer.You will be 
taking the transcript text and summarizing the entire video and
 providing the important summary in points within 250 words. The transcript text will be appended here"""


#Getting the transcript data from youtube
def extract_transcript_details(youtube_video_url):
    try:
        video_id=youtube_video_url.split("=")[1]

        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)
        #print(video_id)

        transcript = ""
        for i in transcript_text:
            transcript+= " " + i["text"]
        return transcript
    except Exception as e:
        raise e

#getting the summary based on Prompt from Google Gemini Pro
def generate_gemini_content(transcript_text,prompt):
    model=genai.GenerativeModel("gemini-1.5-flash")
    response=model.generate_content(prompt+transcript_text)
    return response.text

st.title("YouTube video to detailed notes conveter")
youtube_link = st.text_area("Enter YouTube Video Link: ")

if youtube_link:
    video_id=youtube_link.split("=")[1]
    print(video_id)
    #st.image(f"htto://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

if st.button("Get Detailed Notes"):
    transcript_text=extract_transcript_details(youtube_link)

    if transcript_text:
        summary=generate_gemini_content(transcript_text,prompt)
        st.markdown('Detailed Notes')
        st.write(summary)