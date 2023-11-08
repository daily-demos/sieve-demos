from config import get_upload_dir_path
import sieve
import os
from moviepy.editor import VideoFileClip, AudioFileClip

def extract_audio(source_video: sieve.Video):
    import subprocess
    audio_path = 'temp.wav'
    subprocess.run(["ffmpeg", "-i", source_video.path, audio_path, "-y"])
    return sieve.Audio(path=audio_path)

def audio_enhance(audio:sieve.Audio):
    filter_type = "all"
    enhance_speed_boost = False
    enhancement_steps = 50
    audio_enhancement = sieve.function.get("sieve/audio_enhancement:7954393")
    return audio_enhancement.run(audio, filter_type, enhance_speed_boost, enhancement_steps)

def replaced_audio(video_path: str, audio_path: str):
    video_clip = VideoFileClip(video_path)
    audio_clip = AudioFileClip(audio_path)
    return video_clip.set_audio(audio_clip)

def get_new_video_path(vid_id: str, file_type: bool):
    file_name = f'{vid_id}.{file_type}' # mp4 or json
    return os.path.join(get_upload_dir_path(), file_name)