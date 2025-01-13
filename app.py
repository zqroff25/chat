import streamlit as st
import pandas as pd
from datetime import datetime
import random

# Sayfa yapılandırması
st.set_page_config(
    page_title="Mesajlaşma Uygulaması",
    page_icon="💬",
    layout="centered"
)

# Otomatik yanıtlar listesi
AUTO_RESPONSES = [
    "Merhaba! Size nasıl yardımcı olabilirim?",
    "Bu konuda size yardımcı olmaktan mutluluk duyarım.",
    "Anlıyorum, devam edin lütfen.",
    "İlginç bir bakış açısı!",
    "Bunu biraz daha açıklayabilir misiniz?",
    "Kesinlikle katılıyorum!",
    "Bu konuda size birkaç öneri sunabilirim.",
    "Harika bir soru!",
]

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
    box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
}
.other-message {
    background-color: #424242;
    margin-left: 5%;
    margin-right: 20%;
    box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
}
.timestamp {
    font-size: 0.8em;
    opacity: 0.7;
    margin-top: 5px;
}
.chat-container {
    background-color: #f5f5f5;
    padding: 20px;
    border-radius: 10px;
    margin: 10px 0;
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
if 'bot_name' not in st.session_state:
    st.session_state.bot_name = 'Asistan'

# Kullanıcı adı girişi
if not st.session_state.user_name:
    with st.form("user_form"):
        user_name = st.text_input("Kullanıcı adınızı girin:")
        submit_button = st.form_submit_button("Başla")
        if submit_button and user_name:
            st.session_state.user_name = user_name
            # Hoş geldin mesajı
            welcome_message = {
                "message": f"Merhaba {user_name}! Ben {st.session_state.bot_name}. Size nasıl yardımcı olabilirim?",
                "is_user": False,
                "timestamp": datetime.now().timestamp(),
                "user": st.session_state.bot_name
            }
            st.session_state.messages.append(welcome_message)
            st.rerun()

# Ana mesajlaşma arayüzü
if st.session_state.user_name:
    st.write(f"Hoş geldin, {st.session_state.user_name}! 👋")
    
    # Mesaj konteynerini oluştur
    with st.container():
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        # Mesajları görüntüleme
        for msg in st.session_state.messages:
            message_class = "user-message" if msg["is_user"] else "other-message"
            timestamp = datetime.fromtimestamp(msg["timestamp"]).strftime("%H:%M")
            st.markdown(
                f"""<div class="message-container {message_class}">
                    <b>{msg["user"]}</b><br>
                    {msg["message"]}
                    <div class="timestamp">{timestamp}</div>
                    </div>""",
                unsafe_allow_html=True
            )
        st.markdown('</div>', unsafe_allow_html=True)

    # Mesaj gönderme formu
    with st.form("message_form", clear_on_submit=True):
        user_input = st.text_input("Mesajınız:", key="user_message")
        col1, col2 = st.columns([4, 1])
        with col2:
            send_button = st.form_submit_button("Gönder")
        
        if send_button and user_input:
            # Kullanıcı mesajını kaydet
            user_message = {
                "message": user_input,
                "is_user": True,
                "timestamp": datetime.now().timestamp(),
                "user": st.session_state.user_name
            }
            st.session_state.messages.append(user_message)
            
            # Asistan yanıtını oluştur
            bot_response = {
                "message": random.choice(AUTO_RESPONSES),
                "is_user": False,
                "timestamp": datetime.now().timestamp() + 1,
                "user": st.session_state.bot_name
            }
            st.session_state.messages.append(bot_response)
            st.rerun()

    # Mesajları temizleme butonu
    if st.button("Sohbeti Temizle"):
        st.session_state.messages = []
        st.rerun() 
