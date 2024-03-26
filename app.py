import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from PIL import Image

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input_prompt, image_bytes):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input_prompt, image_bytes])
    return response.text

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        image_bytes = uploaded_file.read()
        return image_bytes
    else:
        raise FileNotFoundError("No file uploaded")

st.set_page_config(page_title="Gemini Health App")
st.header("Gemini Health App")

uploaded_file = st.file_uploader("Choose an image...", type=["JPG", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)
    
submit = st.button("Tell me about the total calories")

input_prompt = """
You are an expert in nutritionist where you need to see the food items from the image and calculate the total calories and Total Protein. 
Also, provide the details of every food item with calories intake in the below format:
1. Item 1 - no of calories and no of Protein
2. Item 2 - no of calories and no of Protein
----
Finally, you can also mention whether the food is healthy or not.
"""

if submit:
    if uploaded_file is None:
        st.error("Please upload an image before submitting.")
    else:
        response = get_gemini_response(input_prompt, image)
        st.header("The Response is")
        st.write(response)
