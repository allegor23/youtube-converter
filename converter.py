import yt_dlp
import os

# Carpeta donde se guardan los MP3s
DOWNLOADS_FOLDER = "downloads"

def crear_carpeta_downloads():
    """Crea la carpeta downloads si no existe"""
    if not os.path.exists(DOWNLOADS_FOLDER):
        os.makedirs(DOWNLOADS_FOLDER)

def obtener_info(url: str):
    """Obtiene información del video sin descargarlo"""
    opciones = {
        'quiet': True,
        'no_warnings': True,
    }
    with yt_dlp.YoutubeDL(opciones) as ydl:
        info = ydl.extract_info(url, download=False)
        return {
            'titulo': info['title'],
            'duracion': info['duration'],
            'thumbnail': info['thumbnail'],
            'uploader': info['uploader'],
        }

def convertir_a_mp3(url: str):
    """Descarga y convierte el audio a MP3"""
    crear_carpeta_downloads()
    
    opciones = {
        'format': 'bestaudio/best',
        'outtmpl': f'{DOWNLOADS_FOLDER}/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True,
        'no_warnings': True,
    }
    
    with yt_dlp.YoutubeDL(opciones) as ydl:
        info = ydl.extract_info(url, download=True)
        titulo = info['title']
        archivo = f"{DOWNLOADS_FOLDER}/{titulo}.mp3"
        return archivo, titulo