import os
import streamlit as st
from video_processor import process_video
from analyze_api import analyzebyGPT, analyze_by_gemini
from object_counter import count_objects, plot_object_distribution,plot_scatter
from clustering_plot import parse_text_file_for_clustering, cluster_data, plot_clusters

st.title("Video Analysis")


st.sidebar.header("Configuration")
api_choice = st.sidebar.selectbox("Select API for Analysis", ["OpenAI GPT", "Gemini"])
output_dir = os.getcwd()  


uploaded_video = st.file_uploader("Upload a Video", type=["mp4", "avi", "mov"])
if uploaded_video is not None:
    
    input_video_path = os.path.join(output_dir, uploaded_video.name)
    with open(input_video_path, "wb") as f:
        f.write(uploaded_video.read())

    st.success(f"Uploaded video saved at {input_video_path}")

    
    if st.button("Process Video"):
        st.info("Processing video, please wait...")
        output_video_path, output_text_path = process_video(input_video_path, output_dir)
        st.success(f"Processing complete. Output video saved at {output_video_path}")
        st.success(f"Output text file saved at {output_text_path}")

        
        st.video(output_video_path)

        
        st.info(f"Analyzing output text using {api_choice} API...")
        output_summary_path = os.path.join(output_dir, "summary.txt")
        if api_choice == "OpenAI GPT":
            analysis_result = analyzebyGPT(output_text_path, output_summary_path)
        else:
            analysis_result = analyze_by_gemini(output_text_path, output_summary_path)

        st.success(f"Analysis complete. Summary saved at {output_summary_path}")
        st.text_area("Summary", analysis_result, height=300)

        st.info("Counting objects from text file...")
        try:
             object_counts = count_objects(output_text_path)
             if object_counts:
                graph_path = os.path.join(output_dir, "object_distribution.png")
                plot_object_distribution(object_counts, graph_path)
                st.image(graph_path, caption="Object Count Distribution")
             else:
                st.warning("No objects found in the text file.")
        except Exception as e:
            st.error(f"Error counting objects: {e}")

        st.info("Generating scatter plot of objects...")
        try:
             scatter_path = os.path.join(output_dir, "scatter_plot.png")
             plot_scatter(object_counts, scatter_path)
             st.image(scatter_path, caption="Scatter Plot of Object Counts")
        except Exception as e:
            st.error(f"Error generating scatter plot: {e}")

            
        st.info("Performing clustering on the text data...")


        if "n_clusters" not in st.session_state:
            st.session_state.n_clusters = 5
            n_clusters = 5
            
        try:
            df = parse_text_file_for_clustering(output_text_path)
            cluster_labels, reduced_data = cluster_data(df, n_clusters=n_clusters)
            cluster_plot_path = os.path.join(output_dir, "cluster_plot.png")
            plot_clusters(reduced_data, cluster_labels, cluster_plot_path)
            st.image(cluster_plot_path, caption="Clustering Visualization")
            df['Cluster'] = cluster_labels
            st.write("Clustered Data:")
            st.dataframe(df)
            st.success("Clustering completed successfully!")
        except Exception as e:
            st.error(f"Error during clustering: {e}")





        st.success("Video Analysis complete!")