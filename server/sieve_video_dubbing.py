import sieve

def extract_audio(source_video: sieve.Video):
    import subprocess
    audio_path = 'temp.wav'
    subprocess.run(["ffmpeg", "-i", source_video.path, audio_path, "-y"])
    return sieve.Audio(path=audio_path)

def transcript_to_text(transcript):
    text = " ".join([segment["text"] for segment in transcript])
    return text

@sieve.function(
    name="video-dubber",
    python_packages=[
        "numpy>=1.19.0",
    ],
    system_packages=["ffmpeg"],
)
def video_dubbing(source_video: sieve.Video, language: str):
    """
    :param source_video: The video to dub
    :param language: The language to dub the video in
    :return: The dubbed video
    """

    print("extracting audio from video")
    # Extract audio from video
    source_audio = extract_audio(source_video)
    print("done extracting")

    # check if language is supported
    if language not in ["english", "spanish", "french", "german", "italian", "portuguese", "polish", "turkish", "russian", "dutch", "czech", "arabic", "chinese"]:
        raise Exception("Language not supported")

    # use remote sieve models
    transcriber = sieve.function.get("sieve/speech_transcriber")
    translator = sieve.function.get("sieve/seamless_text2text")
    tts = sieve.function.get("sieve/xtts-v1")
    lipsyncer = sieve.function.get("sieve/video_retalking")

    print("transcribing audio")
    # transcribe audio
    transcript = list(transcriber.run(source_audio))
    text = transcript_to_text(transcript)
    text_language = "english"
    print("transcription:", text)

    print("translating text")
    # Translate text
    translated_text = translator.run(text, text_language, language)
    print("translated text:", translated_text)

    print("generating tts audio")
    # Generate new audio from translated text
    target_audio = tts.run(translated_text, source_audio, stability=0.5, similarity_boost=0.5)
    print("done generating audio")

    print("starting lipsync")
    # Combine audio and video with Retalker
    return lipsyncer.run(source_video, target_audio)

if __name__ == "__main__":
    video = sieve.Video(url="https://storage.googleapis.com/mango-public-models/david.mp4")
    dubbed_video = video_dubbing.run(video, "spanish")
    print('dubbed video path: ', dubbed_video.path)
