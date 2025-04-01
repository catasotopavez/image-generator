import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
from PIL import Image
import os

# Cargar variables de entorno
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# Título
st.set_page_config(layout="wide")
st.title("🧠 Editor Asistido por IA para Imágenes de Marketing")

# Subida de imagen
st.sidebar.header("📤 Subir imagen")
imagen = st.sidebar.file_uploader("Carga una imagen para editar", type=["jpg", "jpeg", "png"])

# Inicializar sesión de mensajes
if "mensajes" not in st.session_state:
    st.session_state.mensajes = [
        {"role": "system", "content": "Eres un diseñador experto en marketing visual. Asiste al usuario con ideas, recomendaciones o instrucciones para mejorar la imagen cargada."}
    ]

# Mostrar imagen
if imagen:
    st.image(imagen, caption="Imagen cargada", use_column_width=True)

    # Chat al lado derecho
    col1, col2 = st.columns([2, 3])
    with col2:
        st.subheader("💬 Chat con IA")

        user_input = st.chat_input("Describe qué quieres modificar o pregunta algo...")
        if user_input:
            st.session_state.mensajes.append({"role": "user", "content": user_input})

            # Opcional: describe la imagen al modelo
            image_desc = f"La imagen subida por el usuario tiene estas características: [Nombre: {imagen.name}, Tamaño: {imagen.size}]."

            # Enviar a GPT
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    st.session_state.mensajes[0],
                    {"role": "user", "content": image_desc},
                    *st.session_state.mensajes[1:],
                ]
            )

            assistant_msg = response.choices[0].message.content
            st.session_state.mensajes.append({"role": "assistant", "content": assistant_msg})

        # Mostrar conversación
        for msg in st.session_state.mensajes[1:]:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

else:
    st.info("Sube una imagen en la barra lateral para comenzar.")

