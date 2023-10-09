import streamlit as st
import pandas as pd

import os

import openai

import whisper

import pytube
from pytube import YouTube

from helpers import transcribe_whisper, check_subtitles

st.markdown("<h1>Youtube video summarizer</h1>", unsafe_allow_html=True)
st.write("This is an app that will allow you to summarise youtube video and chat with it")

model = whisper.load_model('base')
transcript = ""


# Sidebar
with st.sidebar:
    user_secret = st.text_input(label=":red[OpenAI API key]",
                                value="",
                                placeholder="",
                                type="password")

    yt_url = st.text_input(label=":red[Youtube URL]", value="", placeholder="", type="default")

# if user_secret and yt_url:
    if yt_url:
        yt_video = YouTube(yt_url)
        v_id = pytube.extract.video_id(yt_url)

        streams = yt_video.streams.filter(only_audio=True)

        stream = streams[0]

        if st.button("Start Analysis"):
            if os.path.exists('youtube_video.mp4'):
                os.remove('youtube_video.mp4')

            if os.path.exists('summary.txt'):
                os.remove('summary.txt')

            if os.path.exists('embeddings.csv'):
                os.remove('embeddings.csv')

            with st.spinner("Downloading video"):
                st.write(yt_video.title)
                st.video(yt_url)

                stream.download(filename="youtube_video.mp4")
                audio = open('youtube_video.mp4', 'rb')
                st.audio(audio, format='audio/mp4')

                # subtitles = check_subtitles(yt_video)

                # if subtitles:
                #     st.success("Found subtitles")
                
                st.success("Started transcription")

                transcript = transcribe_whisper(model)
                # save transcript to file
                with open('transcript.txt', 'w') as f:
                    f.write(transcript)

                st.success("Transcription is done. File saved as transcript.txt")

                # print(transcript)


# tab1, tab2, tab3, tab4, tab5 = st.tabs(["How does this work", "Transcript", "Summary", "Talk to the video", "Embeddings"])
tab1, tab2, tab3, tab4 = st.tabs(["How does this work", "Transcript", "Summary", "Talk to the video"])

# TODO Add description if how this works.
with tab1:
    st.write("This is an app that will allow you to summarise youtube video and chat with them")
    st.write("We use the youtube api or whisper to get the transcript of the video and then use the openai api to summarise the video")
    st.write("We then use the openai api to chat with the video")
    st.write("/n")
    st.write("<h2>How to use</h2>", unsafe_allow_html=True)
    st.write("1. Enter your openai api key in the sidebar - this is only for summarisation and chatting with the video")
    st.write("2. Enter the youtube url of the video you want to summarise")
    st.write("3. Click on the start analysis button")

# TODO Extract transcript of the video using youtube api or whisper
with tab2:
    st.header("Transcript")
    st.write("This is the transcript of the video")
    if (os.path.exists('youtube_video.mp4')):
        audio_file = open('youtube_video.mp4', 'rb')
        audio = audio_file.read()
        st.audio(audio, format='audio/mp4')
    else:
        st.write("No video found")

    if transcript != "":
        st.write(transcript)

# TODO Extract summary of the video using openai api and langchain
with tab3:
    st.header("Summary")
    st.write("This is the summary of the video")
    if (os.path.exists('summary.txt')):
        with open('summary.txt', 'r') as f:
            summary = f.read()
            st.write(summary)
    else:
        st.write("No summary found")

# TODO Build vector DB and chat with the video
with tab4:
    st.header("Talk to the video")
    # user_secret = st.text_input(label=":red[OPENAI API KEY]", placeholder="Enter your openai API key", type="password")

# with tab5:
#     st.header("Embeddings")
#     st.write("This is the embeddings of the video")
#     if (os.path.exists('embeddings.csv')):
#         with open('embeddings.csv', 'r') as f:
#             embeddings = f.read()
#             st.write(embeddings)
#     else:
#         st.write("No embeddings found")

    # if generated not in st.session_state:
    #     st.session_state.generated = False

