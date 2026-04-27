import yt_dlp
import os
import shutil

# Temporary folder for audio files
TEMP_FOLDER = "temp"

def clean_temp_folder():
    """Deletes and recreates the temp folder to remove old files"""
    if os.path.exists(TEMP_FOLDER):
        shutil.rmtree(TEMP_FOLDER)
    os.makedirs(TEMP_FOLDER)

def extract_url(url: str):
    """Cleans YouTube URL and extracts only the video ID part"""
    if "watch?v=" in url:
        video_id = url.split("watch?v=")[1].split("&")[0]
        return f"https://www.youtube.com/watch?v={video_id}"
    return url

def get_info(url: str):
    """Gets video information without downloading"""
    clean_url = extract_url(url)
    options = {
        'quiet': True,
        'no_warnings': True,
    }
    with yt_dlp.YoutubeDL(options) as ydl:
        info = ydl.extract_info(clean_url, download=False)
        return {
            'title': info['title'],
            'duration': info['duration'],
            'thumbnail': info['thumbnail'],
            'uploader': info['uploader'],
        }

def convert_audio(url: str, format: str = 'mp3', quality: str = '192'):
    """Downloads and converts audio to the selected format and quality"""
    clean_url = extract_url(url)
    clean_temp_folder()

    # FLAC does not use bitrate, only MP3/AAC/OGG do
    if format == 'flac':
        postprocessors = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'flac',
        }]
    else:
        postprocessors = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': format,
            'preferredquality': quality,
        }]

    options = {
        'format': 'bestaudio/best',
        'outtmpl': f'{TEMP_FOLDER}/%(title)s.%(ext)s',
        'postprocessors': postprocessors,
        'quiet': True,
        'no_warnings': True,
    }

    with yt_dlp.YoutubeDL(options) as ydl:
        info = ydl.extract_info(clean_url, download=True)
        title = info['title']
        file = f"{TEMP_FOLDER}/{title}.{format}"
        return file, title