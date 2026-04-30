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

def clean_filename(filename: str):
    """Removes characters that are invalid in Windows filenames"""
    invalid_chars = ['\\', '/', ':', '*', '?', '"', '<', '>', '|']
    for char in invalid_chars:
        filename = filename.replace(char, '')
    return filename.strip()

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

def convert_audio(url: str, format: str = 'mp3', quality: str = '192',
                  song_title: str = None, artist: str = None,
                  include_thumbnail: bool = False):
    """
    Downloads and converts audio with user-defined metadata.
    All metadata is stripped except what the user explicitly provides.
    Thumbnail is only embedded if include_thumbnail is True.
    """
    clean_url = extract_url(url)
    clean_temp_folder()

    # Base postprocessors — extract audio
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

    # Add metadata postprocessor with user values
    postprocessors.append({
        'key': 'FFmpegMetadata',
        'add_metadata': True,
    })

    # Embed thumbnail only if user chose to
    if include_thumbnail:
        postprocessors.append({
            'key': 'EmbedThumbnail',
        })

    # Get clean title before downloading
    with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
        raw_info = ydl.extract_info(clean_url, download=False)
        clean_title = clean_filename(raw_info['title'])

    options = {
        'format': 'bestaudio/best',
        'outtmpl': f'{TEMP_FOLDER}/{clean_title}.%(ext)s',
        'postprocessors': postprocessors,
        'quiet': True,
        'no_warnings': True,
        # Strip all metadata from source
        'postprocessor_args': {
            'ffmpeg': [
                '-map_metadata', '-1',  # strip all metadata
                '-metadata', f'title={song_title or ""}',
                '-metadata', f'artist={artist or ""}',
            ]
        },
        # Do not write or embed thumbnail unless user chose to
        'writethumbnail': include_thumbnail,
        'embedthumbnail': include_thumbnail,
    }

    with yt_dlp.YoutubeDL(options) as ydl:
        ydl.extract_info(clean_url, download=True)
        file = f"{TEMP_FOLDER}/{clean_title}.{format}"
        return file, clean_title