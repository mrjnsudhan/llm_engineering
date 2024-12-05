import gradio as gr
from pytube import YouTube
from moviepy.editor import AudioFileClip, concatenate_audioclips
import os

# Function to download and process videos
def download_and_process_videos(video_data):
    clips = []
    for data in video_data:
        url, start_time, end_time = data['url'], data['start_time'], data['end_time']
        yt = YouTube(url)
        audio_stream = yt.streams.filter(only_audio=True).first()
        audio_file = audio_stream.download(filename='audio.mp4')
        
        # Trim the audio
        audio_clip = AudioFileClip(audio_file).subclip(start_time, end_time)
        clips.append(audio_clip)
        
        # Clean up the temporary audio file
        os.remove(audio_file)
    
    # Concatenate all audio clips
    final_clip = concatenate_audioclips(clips)
    final_clip.write_audiofile('final_audio.mp3')
    
    # Clean up individual clips
    for clip in clips:
        clip.close()
    
    return 'final_audio.mp3'

# Function to add video to the list
def add_video(video_data, url, start_time, end_time):
    video_data.append({'url': url, 'start_time': start_time, 'end_time': end_time})
    return video_data, video_data

with gr.Blocks() as demo:
    video_data = gr.State([])
    
    with gr.Row():
        url = gr.Textbox(label="YouTube URL")
        start_time = gr.Textbox(label="Start Time (in seconds)")
        end_time = gr.Textbox(label="End Time (in seconds)")
    
    add_button = gr.Button("Add Video")
    video_list = gr.Dataframe(headers=["URL", "Start Time", "End Time"], datatype=["str", "str", "str"], interactive=False)
    submit_button = gr.Button("Submit")
    
    add_button.click(add_video, inputs=[video_data, url, start_time, end_time], outputs=[video_data, video_list])
    submit_button.click(download_and_process_videos, inputs=video_data, outputs=gr.File(label="Download Merged MP3"))

demo.launch()
