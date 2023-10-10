from langchain import OpenAI
from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain import PromptTemplate

def transcribe_whisper(model):
    output = model.transcribe("youtube_video.mp4", verbose=False)

    transcript = output['text']

    return transcript

def check_subtitles(yt_video):
    try:
        subs = yt_video.captions['a.en']
        srt_subs = subs.generate_srt_captions()
        return srt_subs
    except Exception as e:
        print(e)
        return False

def generate_summary(text, llm, chunk_size=5000, max_tokens=500):
    summary = ""
    
    return summary

map_prompt = """
Write a concise summary of the following:
"{text}"
Summarise according to the following criteria:
- Concise
- Accurate
- Relevant
- No plagiarism
- No quotes
CONCISE SUMMARY:
"""
map_prompt_template = PromptTemplate(template=map_prompt, input_variables=["text"])


combine_prompt = """
Write a concise summary of the following text delimited by triple backquotes.
Return your response in bullet points which covers the key points of the text.
```{text}```
Summarise according to the following criteria:
- Concise
- Accurate
- Relevant
- No plagiarism
- No quotes
BULLET POINT SUMMARY:
"""
combine_prompt_template = PromptTemplate(template=combine_prompt, input_variables=["text"])