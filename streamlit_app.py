import streamlit as st
import cv2
import tempfile
import os
from tqdm import tqdm
from video_reader import open_video
from model_loader import load_model
from frame_processor import process_frame
from video_writer import init_video_writer
from api_client import analyze_with_openai
from config import OPENAI_API_KEY


st.title("Video Processing Dashboard")
st.sidebar.header("Options")


st.sidebar.subheader("Upload and Process Video")
uploaded_video = st.sidebar.file_uploader("Upload Video File", type=["mp4", "avi"])
process_button = st.sidebar.button("Process Video")


if uploaded_video is not None:
    st.video(uploaded_video)
    st.write("Video Uploaded Successfully!")

    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
        temp_file.write(uploaded_video.read())
        temp_video_path = temp_file.name

    if process_button:
        st.write("Initializing Model and Video Processing...")
        with st.spinner("Processing Video... Please Wait"):
            try:
                cap = open_video(temp_video_path)
                model = load_model()

                fps = int(cap.get(cv2.CAP_PROP_FPS))
                width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

                
                output_video_path = temp_video_path + "_out.avi"
                output_text_file = temp_video_path + "_out.txt"
                writer = init_video_writer(output_video_path, width, height, fps)

                frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                frame_progress = st.progress(0)

                with open(output_text_file, 'w') as file:
                    for frame_idx in tqdm(range(frames)):
                        ret, frame = cap.read()
                        if not ret:
                            break

                        
                        frame, objects = process_frame(model, frame)
                        writer.write(frame)
                        file.write(f"Frame {frame_idx + 1}: {','.join(objects)}\n")
                        file.flush()

                        
                        frame_progress.progress((frame_idx + 1) / frames)

                cap.release()
                writer.release()

                st.success("Video Processing Complete!")
                st.write(f"Output Video: {output_video_path}")
                st.write(f"Object List File: {output_text_file}")

                # Display output video
                st.video(output_video_path)

            except Exception as e:
                st.error(f"An error occurred: {e}")


st.sidebar.subheader("Analyze Output Text")
analyze_button = st.sidebar.button("Analyze with GPT")

if analyze_button and uploaded_video:
    st.write("Analyzing Video Frames with GPT...")
    with st.spinner("Analyzing..."):
        try:
            with open(output_text_file, 'r') as file:
                content = file.read()

            
            analysis = analyze_with_openai(content, OPENAI_API_KEY)

            st.success("Analysis Complete!")
            st.write("Summary:")
            st.write(analysis)

            
            summary_file = temp_video_path + "_summary.txt"
            with open(summary_file, 'w') as file:
                file.write(analysis)
            st.write(f"Summary File Saved: {summary_file}")

        except Exception as e:
            st.error(f"Error during analysis: {e}")
