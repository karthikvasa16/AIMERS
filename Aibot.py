import streamlit as st
from PIL import Image
from transformers import BlipProcessor, BlipForQuestionAnswering, pipeline
import requests

# Load the BLIP model and processor
processor = BlipProcessor.from_pretrained("Salesforce/blip-vqa-base")
model = BlipForQuestionAnswering.from_pretrained("Salesforce/blip-vqa-base")

# Load the image captioning pipeline
image_to_text = pipeline("image-to-text", model="nlpconnect/vit-gpt2-image-captioning")

def multi_translate(from_lang, to_lang, text):
    url = "https://rapid-translate-multi-traduction.p.rapidapi.com/t"
    payload = {
        "from": from_lang,
        "to": to_lang,
        "q": text
    }
    headers = {
        "x-rapidapi-key": "e980a51c0dmshfee51235fc71445p1e7438jsnffd9be124e8b",
        "x-rapidapi-host": "rapid-translate-multi-traduction.p.rapidapi.com",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Translation failed", "status_code": response.status_code, "message": response.text}

# Streamlit app
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Visual Q&A Bot", "Multi-Language Translator"])

if page == "Visual Q&A Bot":
    st.title("BLIP Visual Question Answering Conversation Bot")

    # Initialize session state for conversation
    

    # Upload an image
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Load the image
        raw_image = Image.open(uploaded_file).convert('RGB')
        st.image(raw_image, caption='Uploaded Image.', use_column_width=True)

        # Button to describe the image
        if st.button("Describe Image"):
            # Generate description for the image
            description = image_to_text(raw_image)[0]['generated_text']
            st.write(f"**Description:** {description}")

        # Display conversation history
        
        # Ask a new question
        question = st.text_input("Ask a question about the image:")

        if st.button("Ask"):
            if question:
                # Process the image and question
                inputs = processor(raw_image, question, return_tensors="pt")

                # Generate the answer
                out = model.generate(**inputs)

                # Decode the answer
                answer = processor.decode(out[0], skip_special_tokens=True)

                # Update conversation history
                st.success(f"Answer: {answer}")
            else:
                st.write("Please enter a question.")

elif page == "Multi-Language Translator":
    st.title("Multi-Language Translator")

    
    from_lang = st.text_input("Enter the source language (e.g., 'en' for English):")
    to_lang = st.text_input("Enter the target language (e.g., 'ar' for Arabic):")
    text = st.text_area("Enter the text to translate:")

    if st.button("Translate"):
        if from_lang and to_lang and text:
            translation_result = multi_translate(from_lang, to_lang, text)
            if "error" in translation_result:
                st.error(f"Error: {translation_result['message']}")
            else:
                st.success(f"Translation: {translation_result}")
        else:
            st.error("Please fill in all the fields.")
