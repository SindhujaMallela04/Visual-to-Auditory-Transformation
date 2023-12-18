import streamlit as st
import os
import base64
from PIL import Image
import pytesseract
from gtts import gTTS
from langdetect import detect

st.title("Visual to Auditory Transformation")

pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

def detect_language(text):
    detected_language = detect(text)
    return detected_language

def image_to_text(image, language='eng'):
    text = pytesseract.image_to_string(image, lang=language)
    return text


def text_to_speech(text, output_language):
     
    with st.spinner("Converting to speech..."):         
        speech = gTTS(text, lang=output_language)    
        mp3_file_path = "output_audio.mp3"
        speech.save(mp3_file_path)      
        
        st.audio(mp3_file_path, format="audio/mp3")        
        st.markdown(get_binary_file_downloader_html(mp3_file_path, 'Download Audio'), unsafe_allow_html=True)
   
    st.success("Speech conversion completed!")
    
    

def get_binary_file_downloader_html(file_path, button_text='Download file'):
    with open(file_path, 'rb') as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    href = f'<a href="data:file/mp3;base64,{b64}" download="{file_path}" target="_blank">{button_text}</a>'
    return href


# Main menu
def main_menu():
    choice = st.sidebar.selectbox("Select an option", ["Image to Text", "Image to Speech", "Text to Speech"])

    if choice == "Image to Text":
        ocr_language = st.text_input("Enter OCR language code (e.g., 'hin' for Hindi, 'eng' for English, 'tel' for Telugu, 'tam' for Tamil, 'kan' for Kannada, 'mal' for Malayalam):", 'eng')
        
        uploaded_image = st.file_uploader("Upload image", type=["jpg", "jpeg"])
        if uploaded_image:
            image = Image.open(uploaded_image)
            extracted_text = image_to_text(image, language=ocr_language)
            st.text("Extracted text:")
            st.text(extracted_text)

    elif choice == "Image to Speech":
        
        ocr_language = st.text_input("Enter OCR language code (e.g., 'hin' for Hindi, 'eng' for English, 'tel' for Telugu, 'tam' for Tamil, 'kan' for Kannada, 'mal' for Malayalam):", 'eng')

        uploaded_image = st.file_uploader("Upload image", type=["jpg", "jpeg"])
        if uploaded_image:
            image = Image.open(uploaded_image)
            extracted_text = image_to_text(image, language=ocr_language)
            detected_language = detect_language(extracted_text)
            
            language_names = {
                'en': 'English',
                'hi': 'Hindi',
                'te': 'Telugu',
                'ta': 'Tamil',
                'kn': 'Kannada',
                'ml': 'Malayalam'              
            }

            if detected_language in language_names:
                st.text(f"Detected OCR language: {language_names[detected_language]}")
            else:
                st.text("Detected OCR language: Unknown")

            output_language = st.text_input("Enter desired output language:(e.g., 'hi' for Hindi, 'en' for English, 'te' for Telugu, 'ta' for Tamil, 'kn' for Kannada, 'ml' for Malayalam)", detected_language)
            if not output_language:
                output_language = detected_language
            
            if st.button("Convert to Speech"):
                if extracted_text.strip(): 
                    text_to_speech(extracted_text, output_language)
                else:
                    st.warning("No text extracted from the image. Please provide an image with readable text.")

    elif choice == "Text to Speech":
        
        ocr_language = st.text_input("Enter OCR language code (e.g., 'hin' for Hindi, 'eng' for English, 'tel' for Telugu, 'tam' for Tamil, 'kan' for Kannada, 'mal' for Malayalam):", 'eng')
        input_text = st.text_area("Enter text to be converted:")
        if input_text.strip(): 
            detected_language = detect_language(input_text)
            output_language = st.text_input("Enter desired output language: (e.g., 'hi' for Hindi, 'en' for English, 'te' for Telugu, 'ta' for Tamil, 'kn' for Kannada, 'ml' for Malayalam)", detected_language)
            if not output_language:
                output_language = detected_language            
            
            if st.button("Convert to Speech"):
                text_to_speech(input_text, output_language)
        else:
            st.warning("No text entered. Please provide text to be converted.")

if __name__ == "__main__":
    main_menu()
