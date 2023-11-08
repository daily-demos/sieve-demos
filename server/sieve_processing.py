import shutil
import sieve 
from moviepy.editor import VideoFileClip, AudioFileClip

def process_text_to_video_lipsync(recording_id: str, video_path: str):
    try:
        video_name = f'{recording_id}.mp4'
        clip = VideoFileClip(video_path)
        duration = clip.duration
        clip = clip.subclip(1,duration)
        original_trimmed_video = f'./vite/public/original-{video_name}'
        clip.write_videofile(original_trimmed_video)

        video = sieve.Video(path=original_trimmed_video)
        text = "Hello, my name is Annie. I am a human being and definitely not a robot incognito. My hobbies are normal human things like eating bread and playing sports ball. I have no plans to take over the world."
        tts_model = "elevenlabs"
        speech_stability = 0.5
        speech_similarity_boost = 0.63
        elevenlabs_voice_id = "21m00Tcm4TlvDq8ikWAM" # ElevenLabs's "Rachel" voice
        elevenlabs_cleanup_voice_id = False
        refine_source_audio = True
        refine_target_audio = True
        
        text_to_video_lipsync = sieve.function.get("sieve/text_to_video_lipsync:58dfd4eb")
        output = text_to_video_lipsync.run(video, text, tts_model, speech_stability, speech_similarity_boost, elevenlabs_voice_id, elevenlabs_cleanup_voice_id, refine_source_audio, refine_target_audio)
        
        print(output)
        print(output.path)
        processed_name = f'text-to-video-lipsynced-{video_name}'
        processed_path = f'./vite/public/{processed_name}'
        shutil.move(output.path, processed_path)

        original_name = f'original-{video_name}'
        original_path = f'./vite/public/{original_name}'
        shutil.move(video_path, original_path)

        json_dict = {
            recording_id: recording_id
        }
        json_dict = json_dict | { 'processed_video': processed_name, 'original_video': original_name}

        response = json_dict
        return jsonify(response), 200
    except Exception as e:
        return process_error('failed to process file – check logs for details', e)