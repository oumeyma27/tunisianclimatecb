import chatbot as cb
import streamlit as st

data_path = 'tunisian_weather_data.txt'

def main():
    """Main function for the Streamlit app."""
    text = ""
    
    with open(data_path, 'r', encoding='utf-8') as file:
        text = file.read().replace('\n', ' ')

    sentences = cb.preprocess(text)

    st.title('Welcome to Uno!')
    st.subheader("A Tunisian climate chatbot 🌞 🌦️")
    st.write(" Note: This chatbot is still in development and may not provide accurate and refined answers.")
    
    # Get user query
    user_query = st.text_input("Hey there! I'm Uno 😊.\n Feel free to ask me about the Tunisian weather!")
    
    if user_query:
        response = cb.chatbot(user_query, sentences)
        if response:
            st.write(response)
        else:
            st.write("Sorry, I can't give you an accurate answer due to my limited knowledge!")
            st.write("You can alternatively visit the [Tunisian National Institute of Meteorology](http://www.meteo.tn/) for more information.")

if __name__ == '__main__':
    main()