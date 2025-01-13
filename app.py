import streamlit as st
import pandas as pd
from datetime import datetime

# Sayfa yapılandırması
st.set_page_config(
    page_title="Mesajlaşma Uygulaması",
    page_icon="💬",
    layout="centered"
)

# CSS stilleri
st.markdown("""
<style>
.stTextInput > div > div > input {
    border-radius: 20px;
}
.stButton > button {
    border-radius: 20px;
    width: 100%;
}
.message-container {
    padding: 10px;
    margin: 5px 0;
    border-radius: 15px;
    color: white;
}
.user-message {
    background-color: #1976D2;
    margin-left: 20%;
    margin-right: 5%;
}
.other-message {
    background-color: #424242;
    margin-left: 5%;
    margin-right: 20%;
}
</style>
""", unsafe_allow_html=True)

# Başlık
st.title("💬 Mesajlaşma Uygulaması")

# Oturum durumu başlatma
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'user_name' not in st.session_state:
    st.session_state.user_name = ''

# Kullanıcı adı girişi
if not st.session_state.user_name:
    with st.form("user_form"):
        user_name = st.text_input("Kullanıcı adınızı girin:")
        submit_button = st.form_submit_button("Başla")
        if submit_button and user_name:
            st.session_state.user_name = user_name
            st.rerun()

# Ana mesajlaşma arayüzü
if st.session_state.user_name:
    st.write(f"Hoş geldin, {st.session_state.user_name}! 👋")
    
    # Mesajları görüntüleme
    for msg in st.session_state.messages:
        message_class = "user-message" if msg["is_user"] else "other-message"
        st.markdown(
            f"""<div class="message-container {message_class}">
                <b>{msg["user"]}</b><br>
                {msg["message"]}
                </div>""",
            unsafe_allow_html=True
        )

    # Mesaj gönderme formu
    with st.form("message_form", clear_on_submit=True):
        user_input = st.text_input("Mesajınız:", key="user_message")
        col1, col2 = st.columns([4, 1])
        with col2:
            send_button = st.form_submit_button("Gönder")
        
        if send_button and user_input:
            # Yeni mesajı kaydet
            new_message = {
                "message": user_input,
                "is_user": True,
                "timestamp": datetime.now().timestamp(),
                "user": st.session_state.user_name
            }
            st.session_state.messages.append(new_message)
            st.rerun()

    # Mesajları temizleme butonu
    if st.button("Sohbeti Temizle"):
        st.session_state.messages = []
        st.rerun() 
