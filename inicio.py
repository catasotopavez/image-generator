import streamlit as st
from openai import OpenAI
from PIL import Image
import requests
from io import BytesIO
import os
from dotenv import load_dotenv

# Cargar API Key desde archivo .env
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Inicializa el cliente de OpenAI
client = OpenAI(api_key=api_key)

# Título de la app
st.title("🖼️ Generador de Imágenes con IA")

# Input del usuario
prompt = st.text_input("Describe tu imagen (en inglés o español):")

# Botón para generar
if st.button("Generar Imagen"):
    if prompt:
        with st.spinner("🧠 Mejorando el prompt..."):
            # Mejora del prompt con GPT
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Eres un experto en crear prompts para generar imágenes con IA."},
                    {"role": "user", "content": f"Mejora este prompt para generar una imagen con DALL·E: {prompt}"}
                ]
            )
            improved_prompt = response.choices[0].message.content.strip()

        st.success("✅ Prompt mejorado:")
        st.markdown(f"**{improved_prompt}**")

        # Generar imagen
        with st.spinner("🎨 Generando imagen..."):
            image_response = client.images.generate(
                model="dall-e-3",
                prompt=improved_prompt,
                n=1,
                size="1024x1024"
            )

            image_url = image_response.data[0].url
            image = Image.open(BytesIO(requests.get(image_url).content))
            st.image(image, caption=improved_prompt)
    else:
        st.warning("Por favor escribe un prompt primero.")
