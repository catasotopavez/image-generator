import streamlit as st
from openai import OpenAI
from PIL import Image
import requests
from io import BytesIO
import os
from dotenv import load_dotenv

# Cargar la clave API
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

st.title("🖼️ Generador de Imágenes con Estilo")

# Input del usuario
prompt = st.text_input("Describe tu imagen (en español o inglés):")

# Selector de estilo
estilo = st.selectbox("Selecciona un estilo artístico:", [
    "Realista",
    "Ilustración digital",
    "Estilo anime",
    "Pintura al óleo",
    "Pixel art",
    "Arte abstracto"
])

# Botón para generar
if st.button("Generar Imagen"):
    if prompt:
        with st.spinner("🧠 Mejorando el prompt con estilo..."):
            prompt_con_estilo = f"{prompt}. Generar en estilo: {estilo.lower()}."

            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Eres un experto en crear prompts para generar imágenes con DALL·E."},
                    {"role": "user", "content": f"Mejora este prompt para generar una imagen con DALL·E: {prompt_con_estilo}"}
                ]
            )
            improved_prompt = response.choices[0].message.content.strip()

        st.success("✅ Prompt mejorado:")
        st.markdown(f"**{improved_prompt}**")

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
