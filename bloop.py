import sieve

def extract_audio(source_video: sieve.Video):
    import subprocess
    audio_path = 'temp.wav'
    subprocess.run(["ffmpeg", "-i", source_video.path, audio_path, "-y"])
    return sieve.Audio(path=audio_path)

def transcript_to_text(transcript):
    print(transcript)
    transcript = [segment for sublist in transcript for segment in sublist]
    text = " ".join([segment["text"] for segment in transcript])
    print(text)
    return text

seamless_language_map = {
    "en": "eng",
    "es": "spa",
    "fr": "fra",
    "de": "deu",
    "it": "ita",
    "pt": "por",
    "pl": "pol",
    "tr": "tur",
    "ru": "rus",
    "nl": "nld",
    "cs": "ces",
    "ar": "ara",
    "zh-cn": "cmn"
}

@sieve.function(
    name="video-dubber",
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
    if language not in ["en", "es", "fr", "de", "it", "pt", "pl", "tr", "ru", "nl", "cs", "ar", "zh-cn"]:
        raise Exception("Language not supported")

    # use remote sieve models
    transcriber = sieve.function.get("sieve/speech_transcriber")
    # translator = sieve.function.get("sieve/seamless_text2text")
    # tts = sieve.function.get("sieve/xtts-v1")
    # lipsyncer = sieve.function.get("sieve/video_retalking")

    print("transcribing audio")
    # transcribe audio
    transcript = list(transcriber.run(source_audio))
    text = transcript_to_text(transcript)
    print("transcription:", text)

    # print("translating text")
    # # Translate text
    # translated_text = translator.run(text, "eng", seamless_language_map[language])
    # print("translated text:", translated_text)

    # print("generating tts audio")
    # # Generate new audio from translated text
    # target_audio = tts.run(source_audio, language, translated_text)
    # print("done generating audio")

    # print("starting lipsync")
    # # Combine audio and video with Retalker
    # return lipsyncer.run(source_video, target_audio)

if __name__ == "__main__":
    video = sieve.Video(url="https://storage.googleapis.com/mango-public-models/david.mp4")
    dubbed_video = video_dubbing.run(video, "es")
    # print('dubbed video path: ', dubbed_video.path)
