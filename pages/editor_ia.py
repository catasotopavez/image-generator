import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
from PIL import Image
import os

# Configuración general
st.set_page_config(page_title="Editor IA", layout="wide")

# Cargar API Key
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# Título centrado
st.markdown("<h1 style='text-align: center;'>🧠 Editor Asistido por IA para Imágenes de Marketing</h1>", unsafe_allow_html=True)

# Inicializar sesión de mensajes e imagen
if "mensajes" not in st.session_state:
    st.session_state.mensajes = [
        {"role": "system", "content": "Eres un diseñador experto en marketing visual. Asiste al usuario con ideas, recomendaciones o instrucciones para mejorar la imagen cargada."}
    ]

if "imagen_cargada" not in st.session_state:
    st.session_state.imagen_cargada = None

# Subida de imagen (pantalla inicial)
if not st.session_state.imagen_cargada:
    st.markdown("### 📤 Sube tu imagen para comenzar", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Carga una imagen (JPG, PNG)", type=["jpg", "jpeg", "png"], label_visibility="collapsed")
    
    if uploaded_file:
        st.session_state.imagen_cargada = uploaded_file
        st.rerun()

# Si hay imagen cargada
else:
    imagen = st.session_state.imagen_cargada
    st.image(imagen, caption="🖼️ Imagen cargada", use_container_width=True)

    # Botón para borrar imagen y resetear chat
    st.markdown("#### ⚙️ Opciones", unsafe_allow_html=True)
    if st.button("🗑️ Borrar imagen y subir otra"):
        st.session_state.imagen_cargada = None
        st.session_state.mensajes = [
            {"role": "system", "content": "Eres un diseñador experto en marketing visual. Asiste al usuario con ideas, recomendaciones o instrucciones para mejorar la imagen cargada."}
        ]
        st.rerun()

    # Layout con columnas: chat a la derecha
    col1, col2 = st.columns([2, 3])

    with col2:
        st.subheader("💬 Chat con IA")

        user_input = st.chat_input("Describe qué quieres modificar o pregunta algo...")

        if user_input:
            st.session_state.mensajes.append({"role": "user", "content": user_input})

            image_desc = f"La imagen subida por el usuario se llama '{imagen.name}'."

            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    st.session_state.mensajes[0],
                    {"role": "user", "content": image_desc},
                    *st.session_state.mensajes[1:]
                ]
            )

            reply = response.choices[0].message.content.strip()
            st.session_state.mensajes.append({"role": "assistant", "content": reply})

        # Mostrar historial del chat
        for msg in st.session_state.mensajes[1:]:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
