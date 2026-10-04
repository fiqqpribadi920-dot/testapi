import streamlit as st
from openai import OpenAI
import os

# 1. Mengambil API Key secara aman dari Cloud Secrets
api_key = os.environ.get("OPENAI_API_KEY")

if not api_key:
    st.error("API Key belum dikonfigurasi di server Secrets!")
else:
    # Inisialisasi client OpenAI
    client = OpenAI(api_key=api_key)

    st.title("🤖 OpenAI GPT Milikku")
    st.write("Selamat datang! Silakan mengobrol dengan AI buatan saya.")

    # 2. Membuat sistem memori chat (Chat History)
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Menampilkan pesan-pesan sebelumnya di layar
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 3. Menerima input chat dari user
    if prompt := st.chat_input("Tanya sesuatu ke GPT..."):
        # Tampilkan chat user di layar
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Ambil respon dari OpenAI API
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            with st.spinner("GPT sedang berpikir..."):
                try:
                    # Memanggil model gpt-4o-mini (bisa diganti ke "gpt-4o" jika mau yang lebih cerdas)
                    response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": m["role"], "content": m["content"]}
                            for m in st.session_state.messages
                        ]
                    )
                    ai_response = response.choices[0].message.content
                    message_placeholder.markdown(ai_response)
                    
                    # Simpan respon AI ke dalam history
                    st.session_state.messages.append({"role": "assistant", "content": ai_response})
                except Exception as e:
                    st.error(f"Terjadi kesalahan pada API: {e}")
                    
