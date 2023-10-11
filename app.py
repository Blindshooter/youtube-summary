import streamlit as st
import pandas as pd

import os

import openai

import whisper

import pytube
from pytube import YouTube


from langchain.llms import OpenAI
# from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import ConversationalRetrievalChain
# from langchain.chat_models import ChatOpenAI
# from langchain.document_loaders import UnstructuredFileLoader
# from langchain.document_loaders.image import UnstructuredImageLoader
# from langchain.document_loaders import ImageCaptionLoader
# from langchain.docstore.document import Document

from helpers import transcribe_whisper, generate_summary, get_embeddings

# from langchain.chains.summarize import load_summarize_chain
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.prompts import PromptTemplate

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
                # TRANSCRIPT TAKES A LONG TIME

                # transcript = transcribe_whisper(model)

                with open("transcript.txt") as f:
                    transcript = f.read()

                # save transcript to file
                with open('transcript.txt', 'w') as f:
                    f.write(transcript)

                st.success("Transcription is done. File saved as transcript.txt")

                # print(transcript)


# tab1, tab2, tab3, tab4, tab5 = st.tabs(["How does this work", "Transcript", "Summary", "Talk to the video", "Embeddings"])
tab1, tab2, tab3, tab4 = st.tabs(["How does this work", "Transcript", "Summary", "Talk to the video"])

with tab1:
    st.write("This is an app that will allow you to summarise youtube video and chat with them")
    st.write("We use the youtube api or whisper to get the transcript of the video and then use the openai api to summarise the video")
    st.write("We then use the openai api to chat with the video")
  
    st.write("<h2>How to use</h2>", unsafe_allow_html=True)
    st.write("1. Enter your openai api key in the sidebar - this is only for summarisation and chatting with the video")
    st.write("2. Enter the youtube url of the video you want to summarise")
    st.write("3. Click on the start analysis button")

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

with tab3:
    st.header("Summary")
    st.write("This is the summary of the video")
    if transcript != "":
        st.write("Transcript found")
        print(user_secret)

        llm = OpenAI(temperature=0, openai_api_key=user_secret)

        # with st.spinner("Generating summary"):

        summary = generate_summary(transcript, llm)

        with open('summary.txt', 'w') as f:
            f.write(summary)

        st.success("Summary generated")
        st.write(summary)
    else:
        pass

# TODO Build vector DB and chat with the video
with tab4:
    st.header("Talk to the video")
    st.write("This is the chat with the video")

    if "processed_data" not in st.session_state:
    #     documents = []

        # if "past" not in st.session_state:
        #     st.session_state.past = []

        # def get_input():
        #     if user_secret:
        #         st.header("Ask me something about the video")
        #         input_text = st.text_input("Enter your question here", value="", type="default", key = "input_text")
        #         return input_text
        
        # user_input = get_input()
        
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=150)
        document_chunks = text_splitter.split_documents(transcript)

        embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
        vectorstore = Chroma.from_documents(document_chunks, embedding_function)

        # Store the processed data in session state for reuse
        st.session_state.processed_data = {
            "document_chunks": document_chunks,
            "vectorstore": vectorstore
            }
    else:
        # If the processed data is already available, retrieve it from session state
        document_chunks = st.session_state.processed_data["document_chunks"]
        vectorstore = st.session_state.processed_data["vectorstore"]

    qa = ConversationalRetrievalChain.from_llm(llm, vectorstore.as_retriever())

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("Ask your questions?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Query the assistant using the latest chat history
        result = qa({"question": prompt, "chat_history": [(message["role"], message["content"]) for message in st.session_state.messages]})

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            # full_response = ""
            full_response = result["answer"]
            message_placeholder.markdown(full_response + "|")
        message_placeholder.markdown(full_response)
        print(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})

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

