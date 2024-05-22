import streamlit as st
from pathlib import Path
import google.generativeai as genai
import io  # io 모듈을 임포트합니다.

# Google Generative AI 설정
genai.configure(api_key="AIzaSyDomSZI67u6wx5z-auQppjUlQkxZWM-7k8")
generation_config = {
    "temperature": 0.4,
    "top_p": 1,
    "top_k": 32,
    "max_output_tokens": 4096,
}
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]
model = genai.GenerativeModel(model_name="gemini-1.0-pro-vision-latest",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

# Streamlit 앱 설정
st.title("이미지 용도 제안 서비스")

uploaded_file = st.file_uploader("이미지 업로드", type=["png", "jpg", "jpeg"])
if uploaded_file is not None:
    # 업로드된 파일을 메모리에서 직접 읽어옵니다.
    bytes_data = uploaded_file.getvalue()
    st.image(bytes_data, caption="업로드된 이미지", use_column_width=True)

    if st.button("이미지 용도 제안"):
        # 업로드된 이미지의 바이트 데이터를 사용합니다.
        image_parts = [{"mime_type": uploaded_file.type, "data": bytes_data}]
        prompt_parts = ["이미지의 물건을 다양한 용도를 제시해줘. 가장 기본적인 용도부터, 정말 이색적인 사용처도 제시해줘\n\n", image_parts[0], "\n\n"]
        response = model.generate_content(prompt_parts)
        st.write(response.text)
