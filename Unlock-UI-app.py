import streamlit as st
import google.generativeai as gemini
from PIL import Image


# Secret Key
keys = {
    "GOOGLE-API-KEY" : st.secrets["GOOGLE-API-KEY"]
}

# Configure API Key
gemini.configure(api_key= keys["GOOGLE-API-KEY"])

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
        st.write(":blue[Unlock-UI] is your go-to app for unlocking the secrets behind website and app interfaces! \
                With just a simple upload of your UI images, you'll dive into an interactive chat experience like never before. \
                Powered by Gemini-Pro-Vision, our backend magic comprehends every pixel of your design, responding accurately to your questions. \
                Whether you're a designer looking for insights or a curious enthusiast, Unlock-UI is your key to unraveling the mysteries of UI/UX design elements.")
        image_file = st.file_uploader("**Upload an image**.. :point_down:", type=['JPEG', 'JPG', 'PNG'])
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
    Answer the questions asked based on the uploaded image.
    If the question is not related to image and a general conversation such as greetings, "Hi", "Thank you", "Let's meet soon", "see you", "bye", reply according to the greetings
    If you don't know, then reply "Sorry! I didn't get you! Please change the question as related to image :neutral_face:"
    """

    # set up chat input from users
    input = st.chat_input("Your curiosity unlocks insights! Shoot your questions about image here..")

    if input:
        if image == "":
            st.error("Please upload an Image!")
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



