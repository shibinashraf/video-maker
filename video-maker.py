import os
import random
import json
from gtts import gTTS
from moviepy.editor import *
import streamlit as st

def select_random_trivia(data):
    return random.choice(data["questions"])

def generate_video_script(trivia):
    question = trivia["question"]
    answer = trivia["answer"]
    additional_info = trivia["additional_info"]
    
    # You can format the video script template as you like
    video_script = f"Question: {question}\n"
    video_script += f"Answer: {answer}\n"
    video_script += f"Additional Information: {additional_info}\n\n"
    video_script += "Thanks for watching! Don't forget to like and subscribe!"
    
    return video_script

def text_to_speech(text, filename):
    tts = gTTS(text=text, lang="en")
    tts.save(filename)

def generate_video(video_script, audio_path, output_path):
    # Create video frames using the video script
    video_frames = [TextClip(line, fontsize=50, color="white", size=(720, 1280)).set_duration(5)
                    for line in video_script.strip().split('\n')]

    # Concatenate video frames to create the final video
    final_video = concatenate_videoclips(video_frames, method="compose")

    # Load the audio file
    audio = AudioFileClip(audio_path)

    # Set the audio duration to match the video duration
    audio = audio.subclip(0, final_video.duration)

    # Add audio to the video
    final_video = final_video.set_audio(audio)

    # Save the final video to the output path
    final_video.write_videofile(output_path, codec='libx264')

def main():
    st.title("Video Script to Video with Voice-Over")

    # Load trivia data from the database
    with open("questions.json", "r") as file:
        trivia_data = json.load(file)

    # Select a random trivia question
    selected_trivia = select_random_trivia(trivia_data)

    # Generate the video script
    video_script = generate_video_script(selected_trivia)

    # Display the video script in the app
    st.subheader("Video Script:")
    st.text_area("Copy and use the generated video script", video_script, height=200)

    # Convert the text script to voice-over audio
    audio_path = "temp_audio.mp3"
    text_to_speech(video_script, audio_path)

    # Define the output path for the final video
    output_path = "output_video.mp4"

    # Generate the video with text and audio
    generate_video(video_script, audio_path, output_path)

    # Display the generated video
    st.subheader("Generated Video:")
    st.video(output_path)

    # Provide the download link for the video
    st.subheader("Download Video:")
    st.markdown(f'<a href="{output_path}" download="generated_video.mp4">Click here to download the video</a>', unsafe_allow_html=True)

    # Remove the temporary files
    os.remove(audio_path)
    os.remove(output_path)

if __name__ == "__main__":
    main()
