import streamlit as st

# --- CSS personalizado ---
st.markdown("""
    <style>
        .centered {
            text-align: center;
        }
        .big-title {
            font-size: 2.8em;
            font-weight: bold;
            color: #FF914D;
            margin-bottom: 0.2em;
        }
        .subtitle {
            font-size: 1.4em;
            color: #444;
            margin-top: -10px;
        }
        .stButton>button {
            width: 100%;
            height: 3.2em;
            font-size: 1.1em;
        }
    </style>
""", unsafe_allow_html=True)

# --- Título principal ---
st.markdown("""
<div class="centered">
    <p class="big-title">👋 Bienvenid@ a Creative Assistant!</p>
    <p class="subtitle">¿En qué te puedo ayudar hoy?</p>
</div>
""", unsafe_allow_html=True)

# --- Botones en columnas ---
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("✨ Generate from a Prompt"):
        st.switch_page("pages/editor_ia.py")

with col2:
    if st.button("🛠️ Edita una Imagen"):
        st.switch_page("pages/editor_ia.py")

with col3:
    if st.button("🧠 Evaluar una Imagen"):
        st.switch_page("pages/editor_ia.py")

with col4:
    if st.button("💡 Generador de Descripciones"):
        st.switch_page("pages/editor_ia.py")
