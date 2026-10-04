import streamlit as st
import anthropic
import os

# 1. Mengambil API Key secara aman dari Cloud Secrets
api_key = os.environ.get("ANTHROPIC_API_KEY")

if not api_key:
    st.error("API Key belum dikonfigurasi di server Secrets!")
else:
    # Inisialisasi client Anthropic
    client = anthropic.Anthropic(api_key=api_key)

    st.title("🤖 Claude AI Milikku")
    st.write("Selamat datang! Silakan mengobrol dengan AI buatan saya.")

    # 2. Membuat sistem memori chat (Chat History)
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Menampilkan pesan-pesan sebelumnya di layar
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 3. Menerima input chat dari user
    if prompt := st.chat_input("Tanya sesuatu ke Claude..."):
        # Tampilkan chat user di layar
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Ambil respon dari Claude API
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            with st.spinner("Claude sedang berpikir..."):
                try:
                    # Memanggil Claude 3.5 Sonnet
                    response = client.messages.create(
                        model="claude-3-5-sonnet-20241022",
                        max_tokens=1024,
                        messages=[
                            {"role": m["role"], "content": m["content"]}
                            for m in st.session_state.messages
                        ]
                    )
                    ai_response = response.content[0].text
                    message_placeholder.markdown(ai_response)
                    
                    # Simpan respon AI ke dalam history
                    st.session_state.messages.append({"role": "assistant", "content": ai_response})
                except Exception as e:
                    st.error(f"Terjadi kesalahan pada API: {e}")
                    
