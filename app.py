import streamlit as st
import os
from converter import get_info, convert_audio, clean_temp_folder

# Page configuration
st.set_page_config(
    page_title="YouTube to MP3",
    page_icon="🎵",
    layout="centered"
)

# Initialize session state
if "initialized" not in st.session_state:
    clean_temp_folder()
    st.session_state.initialized = True
    st.session_state.last_url = None
    st.session_state.audio_data = None
    st.session_state.audio_title = None
    st.session_state.audio_format = None

st.title("🎵 YouTube to MP3 Converter")
st.markdown("Paste a YouTube link and download the audio in your preferred format")

# Format and quality options
format_options = {
    "MP3 - Light (128 kbps)": ("mp3", "128"),
    "MP3 - Standard (192 kbps)": ("mp3", "192"),
    "MP3 - High Quality (320 kbps)": ("mp3", "320"),
    "FLAC - Lossless": ("flac", None),
}
selected_format = st.selectbox("🎼 Format & Quality", list(format_options.keys()))
format_code, quality = format_options[selected_format]

# URL input
url = st.text_input("🔗 YouTube Link", placeholder="https://www.youtube.com/watch?v=...")

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
        with st.spinner("Fetching video information..."):
            info = get_info(url)

        # Display video info
        col1, col2 = st.columns([1, 2])
        with col1:
            st.image(info['thumbnail'], use_container_width=True)
        with col2:
            st.subheader(info['title'])
            st.write(f"**Channel:** {info['uploader']}")
            minutes = info['duration'] // 60
            seconds = info['duration'] % 60
            st.write(f"**Duration:** {minutes}:{seconds:02d}")

        st.divider()

        # Convert button
        if st.button("⬇️ Convert & Download", use_container_width=True):
            with st.spinner(f"Converting to {selected_format}... please wait"):
                file, title = convert_audio(url, format_code, quality)
                # Read file into memory immediately
                with open(file, "rb") as f:
                    st.session_state.audio_data = f.read()
                st.session_state.audio_title = title
                st.session_state.audio_format = format_code

        # Show download button if audio is ready in memory
        if st.session_state.audio_data:
            st.download_button(
                label="📥 Download Audio",
                data=st.session_state.audio_data,
                file_name=f"{st.session_state.audio_title}.{st.session_state.audio_format}",
                mime="audio/mpeg",
                use_container_width=True
            )
            st.success("✅ Conversion successful!")

    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        st.info("Make sure the link is valid and the video is available")