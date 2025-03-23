import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
import openai

load_dotenv()


openai.api_key = os.getenv("OPENAI_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

prompt = """You are a YouTube video summarizer. You will be taking the transcript text
and summarizing the entire video and providing the important summary in points
within 250 words. Please provide the summary of the text given here: """

def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("=")[1]
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)

        transcript = ""
        for i in transcript_text:
            transcript += " " + i["text"]

        return transcript

    except Exception as e:
        if "subtitles are disabled" in str(e).lower():
            raise ValueError("Subtitles are disabled for this video. Please try another video with subtitles enabled.")
        else:
            raise ValueError("An error occurred while retrieving the transcript. Please check the video link and try again.")


def generate_gemini_content(transcript_text, prompt):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt + transcript_text)
    return response.text

def generate_openai_content(transcript_text, prompt):
    response = openai.Completion.create(
        engine="gpt-4o-mini",
        prompt=prompt + transcript_text,
        max_tokens=300,
        temperature=0.7
    )
    return response["choices"][0]["text"].strip()


st.title("YouTube Transcript to Detailed Notes Converter")
youtube_link = st.text_input("Enter YouTube Video Link:")


if youtube_link:
    video_id = youtube_link.split("=")[1]
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_container_width=True)

ai_model = st.radio("Choose AI Model:", ("Gemini", "OpenAI GPT"))

if st.button("Get Detailed Notes"):
    try:
        transcript_text = extract_transcript_details(youtube_link)

        if transcript_text:
            if ai_model == "Gemini":
                summary = generate_gemini_content(transcript_text, prompt)
            elif ai_model == "OpenAI GPT":
                summary = generate_openai_content(transcript_text, prompt)

            st.markdown("## Detailed Notes:")
            st.write(summary)
        else:
            st.error("Could not retrieve transcript text. Please check the video link.")

    except ValueError as ve:
        st.error(str(ve))
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
