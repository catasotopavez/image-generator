import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

# Cargar API Key
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# Inicializar estado
if "input_product" not in st.session_state:
    st.session_state.input_product = ""
if "input_category" not in st.session_state:
    st.session_state.input_category = ""
if "result" not in st.session_state:
    st.session_state.result = ""

# Título
st.markdown("""
<div style="text-align:center">
    <h2 style="color:#FFA500;">💡 Generador de Descripciones</h2>
</div>
""", unsafe_allow_html=True)

# Inputs
product = st.text_input("📦 Ingrese el nombre del producto", key="input_product")
category = st.text_input("🏷️ Ingrese la categoría del producto", key="input_category")

# Botones
col1, col2 = st.columns([1, 0.3])
with col1:
    generar = st.button("🚀 Generar descripción", type="primary")
with col2:
    if st.button("❌ Limpiar"):
        # Limpiar claves seguras (que no son del widget)
        st.session_state.result = ""
        # Forzar recarga para vaciar inputs
        st.session_state.pop("input_product")
        st.session_state.pop("input_category")
        st.rerun()

# Generar descripción
if generar:
    with st.spinner("Generando..."):
        prompt = f"Genera una descripcion para este producto {product}, de esta categoria {category}"
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Eres un generador de descripciones para productos."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        st.session_state.result = response.choices[0].message.content
        st.success("✅ Descripción generada correctamente")

# Mostrar resultado si existe
if st.session_state.result:
    st.markdown(f"""
    <div style="background-color:#f9f9f9;padding:15px 25px;border-radius:10px;border:1px solid #ddd;">
        <h4 style="color:#333;">📄 Descripción generada</h4>
        <p style="color:#444;">{st.session_state.result}</p>
    </div>
    """, unsafe_allow_html=True)
