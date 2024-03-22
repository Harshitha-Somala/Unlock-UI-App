from dotenv import load_dotenv
import streamlit as st
import google.generativeai as gemini
from PIL import Image
import os

load_dotenv()

# Configure API Key
gemini.configure(api_key=os.getenv("GOOGLE_API_KEY")) 

# Load the Gemini Pro Vision model to work with images
model = gemini.GenerativeModel("gemini-pro-vision")

# Function to load inputs and generate results 
# Three arguments: assistant, image and prompt
# assistant: Tell GenAI to work as certain assistant
# image: image used as input about which queries are asked and responses generated
# prompt: query to be answered based on uploaded image
def get_gemini_response(assistant, image, prompt):
    response = model.generate_content([assistant, image, prompt], stream=True)
    response.resolve()
    return response.text
    
# streamlit app
def main():
    st.set_page_config(page_title="Unlock-UI")
    st.header(":black[Unlock-UI Designs :key:]", divider='orange')

    # Check if image exists in session state
    if 'uploaded_image' not in st.session_state:
        st.session_state.uploaded_image = False

    # Initialize empty list to store conversation history in session state
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []
        
    # Sidebar with an About section and file uploader
    with st.sidebar:
        st.subheader("About")   
        st.write(":blue[**Unlock-UI**]: Unveil design secrets effortlessly! Upload your UI images and dive into an interactive chat experience. \
                 Powered by Gemini-Pro-Vision, it comprehends every pixel, delivering accurate insights. Whether you're a designer or enthusiast, \
                 Unlock-UI unlocks the mysteries of UI/UX design elements.")
        
        # referred from https://github.com/wms31/streamlit-gemini/blob/main/app.py
        if 'GOOGLE_API_KEY' in st.secrets:
            st.success('API key already provided!', icon='✅')
            api_key = st.secrets['GOOGLE_API_KEY']
        else:
            api_key = st.text_input('**Enter Google API Key..** ', type='password')
            if not (api_key.startswith('AI')):
                st.warning('Please enter your API Key!', icon='⚠️')
            else:
                st.success('Success!', icon='✅')
        os.environ['GOOGLE_API_KEY'] = api_key
        "[**Get a Google Gemini API key**](https://ai.google.dev/) 	:point_left:"

        image_file = st.file_uploader("**Upload an image**.. ", type=['JPEG', 'JPG', 'PNG'])
        image = ""
        
    # Style the sidebar
    css="""
    <style>
        [data-testid="stSidebar"] {
            background: Orange;
        }
    </style>
    """
    st.write(css, unsafe_allow_html=True)

    # Work with Image uploaded
    if image_file is not None:
        image = Image.open(image_file)
        st.image(image, "Uploaded Image", use_column_width=True)
        st.session_state.uploaded_image = True

    # If image is removed, clear the chat history
    if not image_file and st.session_state.uploaded_image:
        st.session_state.uploaded_image = False
        st.session_state.chat_history = []

    # Initialize assistant's work
    assistant_work = """
    You are an expert in understanding the UI designs. 
    When an image of UI design is uploaded, understand its entire design. 
    Answer the questions accurately.
    If the question is not related to image reply according to the message and a general conversation such as greetings, "Hi", "Thank you", "Let's meet soon", "see you", "bye", "You are wrong", reply according to the greetings
    If you don't know, then reply "Sorry! I didn't get you! Please change the question as related to image :neutral_face:"
    """

    # set up chat input from users
    input = st.chat_input("Your curiosity unlocks insights! Shoot your questions about image here..")

    if input:
        if image == "" and api_key == "":
            st.error(":warning: Please enter an API key and upload an image!")
        elif image == "":
            st.error(":warning: Please upload an image!")
        elif api_key == "":
            st.error(":warning: Please enter an API key!")
        else:
            st.session_state.chat_history.append({"role": "user", "content": input})
            with st.spinner("Generating response..."):
                result = get_gemini_response(assistant_work, image, input)
            st.session_state.chat_history.append({"role": "assistant", "content": result})
            
            # Display chat messages from history on app rerun
            for message in st.session_state.chat_history:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

if __name__=="__main__":
    main()



