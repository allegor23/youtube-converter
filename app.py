import streamlit as st
import os
from converter import get_info, convert_audio, clean_temp_folder

# Page configuration
st.set_page_config(
    page_title="YouTube to Audio",
    page_icon="🎵",
    layout="centered"
)

# Custom CSS - Editorial Classic design
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Jost:wght@300;400;500&display=swap');

/* Main background */
.stApp {
    background-color: #f5f0e8 !important;
}

/* Hide Streamlit default elements */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 3rem !important; max-width: 680px !important; }

/* Title */
.app-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    border-bottom: 2px solid #1a1a18;
    padding-bottom: 20px;
    margin-bottom: 36px;
}
.app-title {
    font-family: 'Playfair Display', serif;
    font-size: 42px;
    font-weight: 700;
    color: #1a1a18;
    line-height: 1.1;
    margin: 0;
}
.app-title em {
    font-style: italic;
    color: #8a5a2a;
}
.app-version {
    text-align: right;
}
.app-version-num {
    font-family: 'Jost', sans-serif;
    font-size: 32px;
    font-weight: 300;
    color: #1a1a18;
    line-height: 1;
}
.app-version-label {
    font-family: 'Jost', sans-serif;
    font-size: 9px;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #8a7a6a;
}

/* Labels */
.field-label {
    font-family: 'Jost', sans-serif;
    font-size: 9px;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #8a7a6a;
    margin-bottom: 4px;
}

/* Streamlit selectbox and input overrides */
.stSelectbox > div > div {
    background-color: transparent !important;
    border: none !important;
    border-bottom: 1.5px solid #1a1a18 !important;
    border-radius: 0 !important;
    color: #1a1a18 !important;
    font-family: 'Jost', sans-serif !important;
    font-size: 14px !important;
    font-weight: 300 !important;
}
.stTextInput > div > div > input {
    background-color: transparent !important;
    border: none !important;
    border-bottom: 1.5px solid #c8b89a !important;
    border-radius: 0 !important;
    color: #1a1a18 !important;
    font-family: 'Jost', sans-serif !important;
    font-size: 13px !important;
    font-weight: 300 !important;
}
.stTextInput > div > div > input::placeholder {
    color: #c8b89a !important;
}
.stTextInput > div > div > input:focus {
    box-shadow: none !important;
    border-bottom: 1.5px solid #8a5a2a !important;
}

/* Video info card */
.video-card {
    background: #1a1a18;
    padding: 20px;
    margin: 24px 0;
    display: flex;
    gap: 20px;
    align-items: center;
}
.video-title {
    font-family: 'Playfair Display', serif;
    font-size: 19px;
    color: #f5f0e8;
    margin: 0 0 4px;
}
.video-meta {
    font-family: 'Jost', sans-serif;
    font-size: 11px;
    color: #8a7a6a;
    letter-spacing: 1px;
}
.video-tag {
    display: inline-block;
    border: 1px solid #8a5a2a;
    color: #8a5a2a;
    font-family: 'Jost', sans-serif;
    font-size: 9px;
    letter-spacing: 2px;
    padding: 2px 8px;
    margin-top: 8px;
    text-transform: uppercase;
}

/* Buttons */
.stButton > button {
    background-color: #1a1a18 !important;
    color: #f5f0e8 !important;
    border: none !important;
    border-radius: 0 !important;
    font-family: 'Jost', sans-serif !important;
    font-size: 10px !important;
    letter-spacing: 3px !important;
    text-transform: uppercase !important;
    padding: 16px !important;
    width: 100% !important;
}
.stButton > button:hover {
    background-color: #8a5a2a !important;
    color: #f5f0e8 !important;
}
.stDownloadButton > button {
    background-color: transparent !important;
    color: #1a1a18 !important;
    border: 1.5px solid #1a1a18 !important;
    border-radius: 0 !important;
    font-family: 'Jost', sans-serif !important;
    font-size: 10px !important;
    letter-spacing: 3px !important;
    text-transform: uppercase !important;
    padding: 16px !important;
    width: 100% !important;
}
.stDownloadButton > button:hover {
    background-color: #1a1a18 !important;
    color: #f5f0e8 !important;
}

/* Success message */
.success-msg {
    font-family: 'Jost', sans-serif;
    font-size: 9px;
    letter-spacing: 3px;
    color: #5a7a5a;
    text-transform: uppercase;
    text-align: center;
    margin-top: 16px;
    border-top: 1px solid #c8b89a;
    padding-top: 16px;
}

/* Error and info messages */
.stAlert {
    border-radius: 0 !important;
    font-family: 'Jost', sans-serif !important;
}

/* Spinner */
.stSpinner > div {
    border-top-color: #8a5a2a !important;
}

/* Divider */
hr {
    border-color: #c8b89a !important;
}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "initialized" not in st.session_state:
    clean_temp_folder()
    st.session_state.initialized = True
    st.session_state.last_url = None
    st.session_state.audio_data = None
    st.session_state.audio_title = None
    st.session_state.audio_format = None

# Header
st.markdown("""
<div class="app-header">
    <h1 class="app-title">YouTube<br>to <em>Audio</em></h1>
    <div class="app-version">
        <div class="app-version-num">v2</div>
        <div class="app-version-label">Converter</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Format and quality options
st.markdown('<div class="field-label">Format & Quality</div>', unsafe_allow_html=True)
format_options = {
    "MP3 — Light (128 kbps)": ("mp3", "128"),
    "MP3 — Standard (192 kbps)": ("mp3", "192"),
    "MP3 — High Quality (320 kbps)": ("mp3", "320"),
    "FLAC — Lossless": ("flac", None),
}
selected_format = st.selectbox("", list(format_options.keys()), label_visibility="collapsed")
format_code, quality = format_options[selected_format]

st.markdown("<br>", unsafe_allow_html=True)

# URL input
st.markdown('<div class="field-label">YouTube Link</div>', unsafe_allow_html=True)
url = st.text_input("", placeholder="https://www.youtube.com/watch?v=...", label_visibility="collapsed")

if url:
    # Clean when URL changes
    if st.session_state.last_url != url:
        clean_temp_folder()
        st.session_state.last_url = url
        st.session_state.audio_data = None
        st.session_state.audio_title = None
        st.session_state.audio_format = None

    try:
        # Fetch video info
        with st.spinner(""):
            info = get_info(url)

        # Video card
        col1, col2 = st.columns([1, 2])
        with col1:
            st.image(info['thumbnail'], use_container_width=True)
        with col2:
            minutes = info['duration'] // 60
            seconds = info['duration'] % 60
            st.markdown(f"""
            <div style="padding-top: 8px;">
                <div class="video-title">{info['title']}</div>
                <div class="video-meta" style="margin-top: 6px;">{info['uploader'].upper()} · {minutes}:{seconds:02d}</div>
                <div class="video-tag">{selected_format}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<hr>", unsafe_allow_html=True)

        # Convert button
        if st.button("⬇ Convert & Download"):
            with st.spinner("Converting..."):
                file, title = convert_audio(url, format_code, quality)
                with open(file, "rb") as f:
                    st.session_state.audio_data = f.read()
                st.session_state.audio_title = title
                st.session_state.audio_format = format_code

        # Download button
        if st.session_state.audio_data:
            st.download_button(
                label="📥 Download Audio",
                data=st.session_state.audio_data,
                file_name=f"{st.session_state.audio_title}.{st.session_state.audio_format}",
                mime="audio/mpeg",
                use_container_width=True
            )
            st.markdown('<div class="success-msg">✓ Conversion successful — ready to download</div>', unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Error: {str(e)}")
        st.info("Make sure the link is valid and the video is available")