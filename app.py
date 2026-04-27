import streamlit as st
import os
from converter import obtener_info, convertir_a_mp3

# Configuración de la página
st.set_page_config(
    page_title="YouTube to MP3",
    page_icon="🎵",
    layout="centered"
)

st.title("🎵 YouTube to MP3 Converter")
st.markdown("Pega el link de un video de YouTube y descarga el audio en MP3")

# Input del link
url = st.text_input("🔗 Link de YouTube", placeholder="https://www.youtube.com/watch?v=...")

if url:
    try:
        # Mostrar info del video
        with st.spinner("Buscando información del video..."):
            info = obtener_info(url)
        
        # Mostrar thumbnail e info
        col1, col2 = st.columns([1, 2])
        with col1:
            st.image(info['thumbnail'], use_container_width=True)
        with col2:
            st.subheader(info['titulo'])
            st.write(f"**Canal:** {info['uploader']}")
            minutos = info['duracion'] // 60
            segundos = info['duracion'] % 60
            st.write(f"**Duración:** {minutos}:{segundos:02d}")
        
        st.divider()
        
        # Botón de conversión
        if st.button("⬇️ Convertir y Descargar MP3", use_container_width=True):
            with st.spinner("Convirtiendo a MP3... esto puede tomar unos segundos"):
                archivo, titulo = convertir_a_mp3(url)
            
            # Botón de descarga
            if os.path.exists(archivo):
                with open(archivo, "rb") as f:
                    st.download_button(
                        label="📥 Descargar MP3",
                        data=f,
                        file_name=f"{titulo}.mp3",
                        mime="audio/mpeg",
                        use_container_width=True
                    )
                st.success("✅ Conversión exitosa!")
            else:
                st.error("❌ Hubo un problema con la conversión")
    
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        st.info("Verifica que el link sea válido y que el video esté disponible")