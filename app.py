from dotenv import load_dotenv
load_dotenv() # to load all environment variables

import streamlit as st
import os
from PIL import Image
import google.generativeai as genai
import speech_recognition as sr

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
genai.configure(api_key=os.environ["API_KEY"])
model1 = genai.GenerativeModel('gemini-pro')

## function to load gemini pro vision
model = genai.GenerativeModel('gemini-pro-vision')

def get_gemini_response(image_data,input_prompt):
    response = model.generate_content([image_data[0], input_prompt])
    ## gemini pro takes the input in form of list
    return response.text

def generate_recipes(input_text):
    # Generate recipes using GPT model
    prompt = f"Generate recipes based on the input: {input_text}"
    response = model1.generate_content(prompt)
    recipes = response.text.split("\n")
    return recipes

def get_voice_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Listening... Click the button again to stop.")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        st.write("Recognizing...")
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        st.error("Sorry, I could not understand your speech.")
        return ""
    except sr.RequestError as e:
        st.error(f"Could not request results from Google Speech Recognition service; {e}")
        return ""

def input_image_details(uploaded_file):
    if uploaded_file is not None:
        # read the file into bytes
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No image uploaded")

st.set_page_config(page_title="IndiChef - Automated Recipe Generator")
st.header("IndiChef - Automated Recipe Generator")


# Apply custom CSS for background image
st.markdown(
    """
    <style>
    .st-emotion-cache-1r4qj8v {
        background-image: url('https://c8.alamy.com/comp/2JDWXK5/food-cooking-background-on-white-table-2JDWXK5.jpg');
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
        font-family: Arial, sans-serif;
    }
    .st-emotion-cache-gh2jqd{
    width: 84%;
    margin-left: 32%;
    padding: 6rem 1rem 10rem;
    max-width: 46rem;
    }
    .header {
        color: #008080;
        text-align: center;
        font-size: 36px;
        margin-bottom: 20px;
    }
    .subheader {
        color: #696969;
        text-align: center;
        font-size: 24px;
        margin-bottom: 10px;
    }
    .button {
        background-color: #008080;
        color: white;
        border-radius: 5px;
        padding: 10px 20px;
        font-size: 18px;
        margin-top: 20px;
        margin-bottom: 20px;
    }
    .error-message {
        color: red;
        text-align: center;
        font-size: 18px;
        margin-top: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)


if st.button("Start Recording"):
    input_text = get_voice_input()
    st.write("You said:", input_text)
    if input_text:
        st.subheader("Generated Recipes:")
        recipes = generate_recipes(input_text)
        for recipe in recipes:
            st.write(recipe)

dish_name = st.text_input("Name of the Dish:", key="dish_name")
input_text = st.text_input("Input Prompt:", key="input")
submit1 = st.button("Tell me about this invoice 1")
uploaded_file = st.file_uploader("Choose an image of the invoice...", type=["jpg", "jpeg", "png"])
image_data = None
if uploaded_file is not None:
    image_data = input_image_details(uploaded_file)
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

submit2 = st.button("Tell me about this invoice 2")

## prompt for gemini
input_prompt = f"Name of the dish: \n\n"
input_prompt += f"You are an expert for giving recipes for Indian dishes.\n\n"
input_prompt += f"Given the uploaded image, please provide the following details:\n\n"
input_prompt += f"- Time required to cook:  minutes\n"
input_prompt += f"- Nature of dish: Vegetarian/Non-vegetarian\n"
input_prompt += f"- Spices and amounts needed:\n"
input_prompt += f"    - Spice 1: [Amount]\n"
input_prompt += f"    - Spice 2: [Amount]\n"
input_prompt += f"    - Spice 3: [Amount]\n"
input_prompt += f"    - ...\n"
input_prompt += f"- Amount of water required: [Amount]\n"
input_prompt += f"- Spiciness level: Spicy/Normal\n\n"
input_prompt += f"Provide a response including these details.\n\n"
input_prompt += f"Lastly, please suggest dishes possible to cook from the uploaded image."

if submit1:
    if input_text:
        st.subheader("Generated Recipes:")
        recipes = generate_recipes(input_text)
        st.write(recipes)
    else:
        st.error("Please enter the input prompt.")

if submit2:
    if image_data is None:
        st.error("Please upload an image.")
    else:
        response = get_gemini_response(image_data, input_prompt)
        st.subheader("The response is")
        st.write(response)

if not input_text:
    st.warning("Please provide an input prompt.")

if input_text:
    st.subheader("Generated Recipes:")
    recipes = generate_recipes(input_text)
    for recipe in recipes:
        st.write(recipe)

