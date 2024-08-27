import moviepy.editor as mp
from pydub import AudioSegment
from pydub.silence import detect_nonsilent
import os

def remove_silence(video_path, output_path, min_silence_len=1000, silence_thresh=-40):
    # Load the video
    video = mp.VideoFileClip(video_path)
    
    # Extract audio from the video
    audio = video.audio
    audio.write_audiofile("temp_audio.wav")
    
    # Load audio file with pydub
    sound = AudioSegment.from_wav("temp_audio.wav")
    
    # Detect non-silent chunks
    non_silent_ranges = detect_nonsilent(sound, 
                                         min_silence_len=min_silence_len, 
                                         silence_thresh=silence_thresh)
    
    # Convert ranges to seconds
    non_silent_ranges_sec = [(start/1000, end/1000) for start, end in non_silent_ranges]
    
    # Cut the video based on these ranges
    clips = [video.subclip(max(start, 0), min(end, video.duration)) 
             for start, end in non_silent_ranges_sec]
    
    # Concatenate the non-silent clips
    final_clip = mp.concatenate_videoclips(clips)
    
    # Determine the codec based on the output file extension
    _, ext = os.path.splitext(output_path)
    if ext.lower() in ['.mp4', '.m4v']:
        codec = 'libx264'
    elif ext.lower() in ['.avi', '.mov']:
        codec = 'mpeg4'
    else:
        codec = 'libx264'  # Default to H.264 codec
        if not ext:
            output_path += '.mp4'  # Add a default extension if missing
    
    # Write the result to a file
    final_clip.write_videofile(output_path, codec=codec)
    
    # Close the video objects to release resources
    video.close()
    final_clip.close()
    
    # Remove the temporary audio file
    os.remove("temp_audio.wav")

# Usage
input_video = "/Users/manuelmao/Downloads/JeremyGiffon.mp4"
output_video = "/Users/manuelmao/Downloads/JeremyGiffonCut.mp4"
remove_silence(input_video, output_video)