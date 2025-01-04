import streamlit as st
import requests

# Set the title of the app
st.title('Todo Chatbot')

# Create a text input for the user
user_input = st.text_input("Ask me anything related to Todos:")

# Display a loading spinner while waiting for the response
if user_input:
    with st.spinner('Waiting for response...'):
        try:
            # Send the user input to your FastAPI chatbot
            response = requests.get(f'http://127.0.0.1:8000/chat/{user_input}', headers={'accept': 'application/json'})
            result = response.json()

            # Reverse the order of messages to display the newest at the top
            for message in reversed(result.get('messages', [])):
                if message['type'] == 'human':
                    st.markdown(f"**You:** {message['content']}")
                elif message['type'] == 'ai':
                    st.markdown(f"**Bot:** {message['content']}")

        except Exception as e:
            st.error("Oops! Something went wrong. Please try again.")

# Display a footer
st.markdown("---")
st.markdown("Built with ❤️ to showcase Todo Chatbot")
