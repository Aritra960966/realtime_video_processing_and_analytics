import streamlit as st
import subprocess


st.title("Video Summarization App")
st.write("This app summarizes the content of YouTube videos and local video files.")


st.header("Choose Summarization Type")

if st.button("YouTube Video Summary generation"):
    subprocess.run(["streamlit", "run", "youtubesummary.py"])

if st.button("Local Video Summary Generation and analytics"):
    subprocess.run(["streamlit", "run", "localvideo.py"])
