"""This module is responsible for all project processing operations."""

import json
import os
import shutil
import sys
import traceback
import uuid
from enum import Enum
from pathlib import Path
import sieve

from config import get_project_temp_dir_path, \
    get_project_output_file_path, \
    get_project_status_file_path
from transcription.timestamp import Timestamps
from transcription import dg, whisper

from moviepy.video.compositing.concatenate import concatenate_videoclips
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip


def extract_audio(source_video: sieve.Video):
    import subprocess
    audio_path = 'temp.wav'
    subprocess.run(["ffmpeg", "-i", source_video.path, audio_path, "-y"])
    return sieve.Audio(path=audio_path)

def transcript_to_text(transcript):
    # transcript = [segment for sublist in transcript for segment in sublist]
    # text = " ".join([segment["text"] for segment in transcript])
    return  transcript[0]["text"]
    # return text

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

class Transcribers(Enum):
    """Class representing an implemented transcriber."""
    WHISPER = whisper
    DEEPGRAM = dg


class Status(Enum):
    """Class representing project processings status."""
    IN_PROGRESS = "In progress"
    FAILED = "Failed"
    SUCCEEDED = "Succeeded"


class Project:
    """Class representing a single filler word removal project."""
    transcriber = None
    id = None

    def __init__(
            self,
            transcriber=None,
    ):
        # if not transcriber:
        #     transcriber = Transcribers.WHISPER
        #     deepgram_api_key = os.getenv("DEEPGRAM_API_KEY")
        #     if deepgram_api_key:
        #         transcriber = Transcribers.DEEPGRAM
        # self.transcriber = transcriber.value
        self.id = self.configure()

    def configure(self):
        """Generates a unique ID for this project and creates its temp dir"""
        proj_id = uuid.uuid4()
        temp_dir = get_project_temp_dir_path(proj_id)
        if os.path.exists(temp_dir):
            # Directory already exists, which indicates a conflict.
            # Pick a new UUID and try again
            return self.configure()
        os.makedirs(temp_dir)
        return proj_id

    # def process(self, source_video_path: str):
        """Processes the source video to remove filler words"""
        self.update_status(Status.IN_PROGRESS, '')
        try:
            self.update_status(Status.IN_PROGRESS, 'Extracting audio')
            audio_file_path = self.extract_audio(source_video_path)
        except Exception as e:
            traceback.print_exc()
            print(e, file=sys.stderr)
            self.update_status(Status.FAILED, 'failed to extract audio file')
            return

        try:
            self.update_status(Status.IN_PROGRESS, 'Transcribing audio')
            result = self.transcribe(audio_file_path)
        except Exception as e:
            traceback.print_exc()
            print(e, file=sys.stderr)
            self.update_status(Status.FAILED, 'failed to transcribe audio')
            return

        try:
            self.update_status(Status.IN_PROGRESS, 'Splitting video file')
            split_times = self.get_splits(result)
        except Exception as e:
            traceback.print_exc()
            print(e, file=sys.stderr)
            self.update_status(Status.FAILED, 'failed to get split segments')
            return

        try:
            self.update_status(Status.IN_PROGRESS, 'Reconstituting video file')
            self.resplice(source_video_path, split_times)
        except Exception as e:
            traceback.print_exc()
            print(e, file=sys.stderr)
            self.update_status(Status.FAILED, 'failed to resplice video')
            return

        self.update_status(Status.SUCCEEDED, 'Output file ready for download')
    
    def video_dubbing(self, source_video: sieve.Video, language: str):
        """
        :param source_video: The video to dub
        :param language: The language to dub the video in
        :return: The dubbed video
        """
        self.update_status(Status.IN_PROGRESS, '')
        print("extracting audio from video")
        # Extract audio from video
        source_audio = extract_audio(source_video)
        print("done extracting")

        # check if language is supported
        if language not in ["en", "es", "fr", "de", "it", "pt", "pl", "tr", "ru", "nl", "cs", "ar", "zh-cn"]:
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
        print("transcription:", text)

        print("translating text")
        # Translate text
        translated_text = translator.run(text, "eng", seamless_language_map[language])
        print("translated text:", translated_text)

        print("generating tts audio")
        # Generate new audio from translated text
        target_audio = tts.run(source_audio, "spanish", translated_text)
        print("done generating audio")
        print(target_audio.path)

        print("starting lipsync")
        # Combine audio and video with Retalker
        lipsynced = lipsyncer.run(source_video, target_audio)
        print(lipsynced.path)
        self.update_status(Status.SUCCEEDED, '')

    def extract_audio(self, video_path: str):
        """Extracts audio from given MP4 file"""
        video = VideoFileClip(video_path)
        audio_file_name = f'{Path(video_path).stem}.wav'
        audio_path = os.path.join(
            get_project_temp_dir_path(self.id), audio_file_name)
        try:
            video.audio.write_audiofile(audio_path)
        except Exception as e:
            raise Exception('failed to save extracted audio file',
                            video_path, audio_path) from e
        return audio_path

    # def transcribe(self, audio_path: str):
    #     """Transcribes given audio file"""
    #     return self.transcriber.transcribe(audio_path)

    # def get_splits(self, result) -> Timestamps:
    #     """Gets approprpiate split points excluding filler words from given transcription"""
        return self.transcriber.get_splits(result)

    # def resplice(self, source_video_path: str, splits: Timestamps):
        """Splits and then reconstitutes given video file at provided split points"""
        tmp = get_project_temp_dir_path(self.id)

        clips = []
        current_split = splits.head
        idx = 0
        try:
            while current_split:
                clip_file_path = os.path.join(tmp, f"{str(idx)}.mp4")
                ffmpeg_extract_subclip(source_video_path, current_split.start, current_split.end,
                                       targetname=clip_file_path)
                clips.append(VideoFileClip(clip_file_path))
                current_split = current_split.next
                idx += 1
        except Exception as e:
            raise Exception('failed to split clips') from e

        try:
            final_clip = concatenate_videoclips(clips)

            output_file_path = get_project_output_file_path(self.id)
            final_clip.write_videofile(
                output_file_path,
                codec='libx264',
                audio_codec='aac',
                fps=60,
            )
        except Exception as e:
            raise Exception('failed to reconcatenate clips') from e

        # Remove temp directory for this project
        shutil.rmtree(tmp)

    def update_status(self, status: Status, info: str):
        """Updates the project's status file"""
        status = {
            'status': status.value,
            'info': info,
        }
        if status is Status.SUCCEEDED:
            status['download_url'] = get_project_output_file_path(self.id)

        status_file_path = get_project_status_file_path(self.id)
        with open(status_file_path, 'w+', encoding='utf-8') as f:
            f.write(json.dumps(status))
