from dotenv import load_dotenv

load_dotenv()

import streamlit as st
import os
import pathlib
import textwrap
from PIL import Image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

#MODEL
model=genai.GenerativeModel("gemini-pro-vision")

def get_gemini_response(input,image,prompt):
    response=model.generate_content([input,image[0],prompt])
    return response.text

def input_image_details(uploaded_file):
    if uploaded_file is not None:
        bytes_data=uploaded_file.getvalue()

        image_parts= [
            {
                "mime_type":uploaded_file.type,
                "data":bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")


#StreamLit

st.set_page_config(page_title="Caption Generator")
st.header("Caption Generator")
input=st.text_input("Enter Prompt",key="input")
uploaded_file=st.file_uploader("Choose image...",type=["jpg","jpeg","png"])

image=""
if uploaded_file is not None:
    image=Image.open(uploaded_file)
    # st.image(image, caption= "Uploaded_Image", use_column_width=True)

submit=st.button("Generate Caption:")
input_prompt="""
               You have to provide 3 captions for the given images in a very aesthetic manner in reference
               to pinterest style and very genZ type. If the user gives prompt add that too
"""

if submit:
    image_data=input_image_details(uploaded_file)
    response=get_gemini_response(input_prompt,image_data,input)
    st.subheader("The generated caption is:")
    st.write(response)