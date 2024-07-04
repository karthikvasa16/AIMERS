import streamlit as st
from pytube import YouTube
from moviepy.editor import VideoFileClip, AudioFileClip
import os

# Helper function to clear temporary files
def clear_temp_files(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)

# Function to download the YouTube video
def download_video(url):
    yt = YouTube(url)
    video = yt.streams.get_highest_resolution()
    video_file_path = video.download(filename='downloaded_video.mp4')
    return video_file_path

# Function to download the audio from the YouTube video
def download_audio(url, output_format='mp3'):
    yt = YouTube(url)
    video = yt.streams.filter(only_audio=True).first()
    audio_file_path = video.download(filename='temp_audio.mp4')

    # Convert to desired audio format
    audio_clip = AudioFileClip(audio_file_path)
    output_file_path = f'output_audio.{output_format}'

    if output_format == 'mp3':
        audio_clip.write_audiofile(output_file_path)
    else:
        st.error("Invalid output format")
        return None

    # Close the audio clip and remove temporary file
    audio_clip.close()
    clear_temp_files(audio_file_path)

    return output_file_path

# Main Streamlit app
def main():
    st.title("YouTube Video/Audio Downloader")

    # User input: YouTube video link
    video_link = st.text_input("Enter the YouTube video link:")

    # User input: Output format for audio
    

    # Download video button
    if st.button("Download Video"):
        if video_link:
            try:
                video_file = download_video(video_link)
                st.success("Video downloaded successfully!")
                st.video(video_file)
            except Exception as e:
                st.error(f"Error occurred: {str(e)}")
        else:
            st.warning("Please enter a YouTube video link.")

    # Download audio button
    if st.button("Download Audio"):
        if video_link:
            try:
                output_format = 'mp3'
                audio_file = download_audio(video_link, output_format)
                st.success("Audio downloaded successfully!")
                st.audio(audio_file, format='audio/' + output_format)
            except Exception as e:
                st.error(f"Error occurred: {str(e)}")
        else:
            st.warning("Please enter a YouTube video link.")

if __name__ == "__main__":
    main()
