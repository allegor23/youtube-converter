# 🎵 YouTube to Audio Converter

A simple and elegant desktop app to extract and download audio from YouTube videos in multiple formats and quality levels.

Built with Python and Streamlit, runs locally on your machine.

---

## Features

- Paste any YouTube link (clean or with playlist parameters)
- Automatic URL cleaner — no need to trim the link manually
- Choose your format and quality before downloading
- Preview video info (title, channel, duration, thumbnail) before converting
- Temp folder auto-cleans on startup and when switching videos
- Edit song name and artist metadata before converting
- Choose to embed or skip cover art (thumbnail) in the audio file
- All source metadata stripped — only user-confirmed tags are saved

## Supported Formats

| Format | Quality | Best For |
|--------|---------|----------|
| MP3 | 128 kbps | Light, small files |
| MP3 | 192 kbps | Standard everyday use |
| MP3 | 320 kbps | High quality listening |
| FLAC | Lossless | Audiophile quality |

---

## Requirements

- Python 3.9+
- FFmpeg installed and added to PATH

## Installation

1. Clone the repository
   ```bash
   git clone https://github.com/allegor23/youtube-converter.git
   cd youtube-converter
   ```

2. Create and activate a virtual environment
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

4. Install FFmpeg
   - Download from https://ffmpeg.org
   - Add the `bin` folder to your system PATH

## Usage

```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501`

---

## Project Structure

```
youtube-converter/
├── app.py           # Streamlit UI
├── converter.py     # yt-dlp audio extraction logic
├── requirements.txt # Python dependencies
└── temp/            # Temporary audio files (auto-cleaned)
```

---

## Tech Stack

- [Streamlit](https://streamlit.io) — UI framework
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) — YouTube audio extraction
- [FFmpeg](https://ffmpeg.org) — Audio conversion
```