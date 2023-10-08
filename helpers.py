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
        print("No subtitles found")
        return False
