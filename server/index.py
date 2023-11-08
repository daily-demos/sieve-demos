"""This module defines all the routes for the filler-word removal server."""
import json
import os
import sys
import traceback
import sieve
import json
import shutil
from moviepy.editor import VideoFileClip, AudioFileClip

from daily import fetch_recordings, get_access_link
from quart_cors import cors
import quart
import requests
from config import ensure_dirs, get_output_dir_path, get_upload_dir_path
from quart import Quart, jsonify, send_from_directory

app = Quart(__name__)
cors(app, allow_origin="http://localhost:5173")
ensure_dirs()
app.config["MAX_CONTENT_LENGTH"]=300777216


@app.route('/text_to_video_lipsync/<recording_id>', methods=['POST'])
async def process_recording_text_to_video_lipsync(recording_id):
    """Processes a Daily recording by given recording ID."""
    access_link = get_access_link(recording_id)

    try:
        data = requests.get(access_link, timeout=10)
    except Exception as e:
        return process_error('failed to download Daily recording', e)

    file_path = get_new_video_path(recording_id, 'mp4')
    try:
        with open(file_path, 'wb') as file:
            file.write(data.content)
    except Exception as e:
        return process_error('failed to save Daily recording file', e)

    return process_text_to_video_lipsync(recording_id, file_path)

@app.route('/audio_enhance/<recording_id>', methods=['POST'])
async def process_recording_audio_enhance(recording_id):
    """Processes a Daily recording by given recording ID."""
    access_link = get_access_link(recording_id)

    try:
        data = requests.get(access_link, timeout=10)
    except Exception as e:
        return process_error('failed to download Daily recording', e)

    file_path = get_new_video_path(recording_id, 'mp4')
    try:
        with open(file_path, 'wb') as file:
            file.write(data.content)
    except Exception as e:
        return process_error('failed to save Daily recording file', e)

    return process_audio_enhance(recording_id, file_path)

@app.route('/video_dubbing/<recording_id>', methods=['POST'])
async def process_recording_video_dubbing(recording_id):
    """Processes a Daily recording by given recording ID."""
    access_link = get_access_link(recording_id)

    try:
        data = requests.get(access_link, timeout=10)
    except Exception as e:
        return process_error('failed to download Daily recording', e)

    file_path = get_new_video_path(recording_id, 'mp4')
    try:
        with open(file_path, 'wb') as file:
            file.write(data.content)
    except Exception as e:
        return process_error('failed to save Daily recording file', e)

    return process_video_dubbing(recording_id, file_path)

def process_audio_enhance(recording_id: str, video_path: str):
    try:

        video = sieve.Video(path=video_path)
        audio = extract_audio(video)
        print(audio)
        output = audio_enhance(audio)
        
        json_dict = {
            recording_id: recording_id
        }
        
        print(output.path)
        video_clip = VideoFileClip(video_path)
        audio_clip = AudioFileClip(output.path)
        final_clip = video_clip.set_audio(audio_clip)
        new_video_path = f'./vite/public/{recording_id}-enhanced.mp4'
        final_clip.write_videofile(new_video_path)
        
        video_name = f'{recording_id}.mp4'
        original_name = f'original-{video_name}'
        original_path = f'./vite/public/{original_name}'
        shutil.move(video_path, original_path)
        
        json_dict = json_dict | { 'processed_video': f'{recording_id}-enhanced.mp4', 'original_video': original_name}

        response = json_dict
        return jsonify(response), 200
    except Exception as e:
        return process_error('failed to process file – check logs for details', e)

def process_video_dubbing(recording_id: str, video_path: str) -> tuple[quart.Response, int]:
    """Runs filler-word-removal processing on given file."""
    try:
        video_name = f'{recording_id}.mp4'
        clip = VideoFileClip(video_path)
        duration = clip.duration
        clip = clip.subclip(1,duration)
        original_name = f'original-{video_name}'
        original_trimmed_video = f'./vite/public/{original_name}'
        clip.write_videofile(original_trimmed_video)

        video = sieve.Video(path=original_trimmed_video)
        path = video_dubbing(video, "spanish")
        processed_name = f'dubbed-{video_name}'
        processed_path = f'./vite/public/{processed_name}'
        shutil.move(path, processed_path)
        json_dict = {
            recording_id: recording_id,
            'original_video': original_name,
            'processed_video': processed_name
        }
        print()

        response = json_dict
        return jsonify(response), 200
    except Exception as e:
        return process_error('failed to process file – check logs for details', e)
    
def process_transcript_analyzer(recording_id: str, video_path: str) -> tuple[quart.Response, int]:
    """Runs filler-word-removal processing on given file."""
    try:
        video = sieve.Video(path=video_path)
        video_transcript_analyzer = sieve.function.get("sieve/video_transcript_analyzer")
        output = video_transcript_analyzer.run(video)
        json_dict = {
            recording_id: recording_id
        }
        json_path = os.path.join(get_upload_dir_path(), f'{recording_id}.json')

        for i, output_object in enumerate(output):
            print(i)
            print(output_object)
            print(type(output_object))
            if i == 2 or i == 3 or i == 4:
                json_dict = json_dict | output_object

        with open(json_path, 'w') as fp:
            json.dump(json_dict, fp)

            response = json_dict
            return jsonify(response), 200
    except Exception as e:
        return process_error('failed to process file – check logs for details', e)

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
    transcriber = sieve.function.get("sieve/speech_transcriber:8eb4cdf")
    translator = sieve.function.get("sieve/seamless_text2text:f8695f6")
    tts = sieve.function.get("sieve/xtts-v1:e788931")
    lipsyncer = sieve.function.get("sieve/video_retalking:de84f40")

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
    return lipsyncer.run(source_video, target_audio).path

@app.route('/projects/<project_id>', methods=['GET'])
async def get_status(project_id):
    """Route to return current processing status of a project."""
    status_file_name = f'{project_id}.txt'
    status_file_path = os.path.join(get_output_dir_path(), status_file_name)
    try:
        with open(status_file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return jsonify(data), 200
    except Exception as e:
        msg = "failed to open status file"
        print(e, file=sys.stderr)
        return jsonify({'error': msg}), 500


@app.route('/projects/<project_id>/download', methods=['GET'])
async def download_final_output(project_id):
    """Route to download final processed output file."""
    output_file_name = f'{project_id}.mp4'
    return await send_from_directory(get_output_dir_path(), output_file_name, as_attachment=True)


@app.route('/recordings', methods=['GET'])
async def get_daily_recordings():
    """Route to fetch all Daily recordings from configured domain."""
    try:
        recordings = fetch_recordings()
        return jsonify({'recordings': recordings}), 200

    except Exception as e:
        msg = "failed to fetch Daily recordings. Is the Daily API key configured?"
        print(msg, e, file=sys.stderr)
        return jsonify({'error': msg}), 500


def process_error(msg: str, error: Exception) -> tuple[quart.Response, int]:
    """Prints provided error and returns appropriately-formatted response."""
    traceback.print_exc()
    print(msg, error, file=sys.stderr)
    response = {'error': msg}
    return jsonify(response), 500

@app.after_serving
async def shutdown():
    for task in app.background_tasks:
        task.cancel()

if __name__ == '__main__':
    app.run(debug=True)
