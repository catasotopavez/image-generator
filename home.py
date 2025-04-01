import streamlit as st

st.set_page_config(layout="centered", page_title="AI Image Studio")

st.markdown("## 👋 Welcome, Catalina!")
st.markdown("### How would you like to start designing?")

col1, col2 = st.columns(2)

with col1:
    if st.button("📷 Start from an Image"):
        st.switch_page("pages/editor_ia.py")

with col2:
    if st.button("✨ Generate from a Prompt"):
        st.switch_page("pages/inicio.py")
