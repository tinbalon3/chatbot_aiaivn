import streamlit as st
from backend_chatbot import chatbot, initialize_data

# Giao diện Streamlit
def main():
    # Tiêu đề
    st.title("Chatbot AI Việt Nam")
    st.write("Hỏi bất kỳ điều gì liên quan đến công nghệ, AI, và hơn thế nữa!")

    # Khởi tạo dữ liệu khi ứng dụng bắt đầu (chỉ chạy một lần)
    if "initialized" not in st.session_state:
        with st.spinner("Đang khởi tạo dữ liệu..."):
            st.write(initialize_data())
            st.session_state.initialized = True

    # Ô nhập liệu cho câu hỏi
    query = st.text_input("Nhập câu hỏi của bạn:", "")

    # Nút gửi câu hỏi
    if st.button("Gửi"):
        if query:
            with st.spinner("Đang xử lý..."):
                response = chatbot(query)
                st.write("**Bot:**", response)
        else:
            st.warning("Vui lòng nhập câu hỏi!")

if __name__ == "__main__":
    main()