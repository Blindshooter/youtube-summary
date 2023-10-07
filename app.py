import streamlit as st
import pandas as pd
import numpy as np
import os

import openai

import whisper

import pytube

st.markdown("<h1>Youtube video summarizer</h1>", unsafe_allow_html=True)
st.write("This is an app that will allow you to summarise youtube video and chat with them")

# VIDEO_DATA = "https://youtu.be/bsFXgfbj8Bc"

# width = 400

# side = 20

# _, container, _ = st.columns([side, 50, side])
# container.video(data=VIDEO_DATA)

# Sidebar
with st.sidebar:
    user_secret = st.text_input(label=":red[OpenAI API key]",
                                value="",
                                placeholder="",
                                type="password")

    yt_url = st.text_input(label=":red[Youtube URL]",
                                value="",
                                placeholder="",
                                type="default")



tab1, tab2, tab3, tab4, tab5 = st.tabs(["How does this work", "Transcript", "Summary", "Embeddings", "Talk to the video"])

with tab1:
    st.write("This is an app that will allow you to summarise youtube video and chat with them")
    st.write("We use the youtube api or whisper to get the transcript of the video and then use the openai api to summarise the video")
    st.write("We then use the openai api to chat with the video")
with tab2:
    st.header("Transcript")
    st.write("This is the transcript of the video")
    if(os.path.exists('youtube_video.mp4')):
        audio_file = open('youtube_video.mp4', 'rb')
        audio = audio_file.read()
        st.audio(audio, format='audio/mp4')
    else:
        st.write("No video found")

with tab3:
    st.header("Summary")
    st.write("This is the summary of the video")
    if(os.path.exists('summary.txt')):
        with open('summary.txt', 'r') as f:
            summary = f.read()
            st.write(summary)
    else:
        st.write("No summary found")
    
with tab4:
    st.header("Embeddings")
    st.write("This is the embeddings of the video")
    if(os.path.exists('embeddings.csv')):
        with open('embeddings.csv', 'r') as f:
            embeddings = f.read()
            st.write(embeddings)
    else:
        st.write("No embeddings found")

with tab5:
    st.header("Talk to the video")
    user_secret = st.text_input(label="[OPENAI API KEY]", placeholder="Enter your openai API key", type = "password")

    # if generated not in st.session_state:
    #     st.session_state.generated = False

