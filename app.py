import os
import csv
import datetime
import nltk
import ssl
import pickle 
import streamlit as st
import random
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# SSL context to avoid download issues
ssl._create_default_https_context = ssl._create_unverified_context
nltk.data.path.append(os.path.abspath("nltk_data"))
nltk.download("punkt")

# Load intents file
with open('intents.json', 'r') as file:
    intents = json.load(file)

# Initialize vectorizer and model
vectorizer = TfidfVectorizer()
clf = LogisticRegression(random_state=0, max_iter=10000)

# Prepare training data
tags = []
patterns = []
for intent in intents:
    for pattern in intent['patterns']:
        tags.append(intent['tags'])
        patterns.append(pattern)

x = vectorizer.fit_transform(patterns)
y = tags
clf.fit(x, y)

# Chatbot response function
def foodiegenie_chatbot(input_text):
    try:
        input_text = vectorizer.transform([input_text])
        tag = clf.predict(input_text)[0]
        for intent in intents:
            if intent['tags'] == tag:
                return random.choice(intent['responses'])
    except Exception as e:
        return "I'm sorry, I couldn't understand that. Could you please rephrase?"

# Streamlit enhancements
counter = 0

def main():
    global counter
    st.title("FoodieGenie🤖: Your Wish✨, Our Dish🍽️")
    st.write("""
    Your personal hotel assistant, here to make your stay more comfortable and your dining experience exceptional!  
    With **FoodieGenie**, simply make a wish and let us handle the rest! 
    Explore the features below to see how we can assist you.  
""")

# Features Overview
st.subheader("Features of FoodieGenie")
st.write("""
- **Instant Dining Orders** 🍕: Order your meals with just a few taps.
- **Room Service Requests** 🛏️: Request extra pillows, towels, or any other service.
- **Personalized Recommendations** 🤖: Based on your preferences, we suggest the best dishes.
- **24/7 Availability** 🌙: We're always here to help, no matter the time!
""")

# Call to Action
st.write("""
    **Ready to get started?**  
    Let **FoodieGenie** assist you right away! 
    Click on the options in the sidebar to start your experience.
""")

# Optional: Chatbot Start Button
if st.button("Start Chatting with FoodieGenie 👨🏻‍🍳"):
    st.write("Hello! I am FoodieGenie, your personal assistant. How can I help you today?")

# Optional: Add an Image or Logo
    st.image('foodie.png', caption="FoodieGenie - Your Personal Assistant")
    # Sidebar menu
    menu = ["Home 🍽", "Conversation History 📂", "About 📝"]
    choice = st.sidebar.selectbox("Menu ", menu)

    # Home
    if choice == "Home":
        st.write("Welcome to FoodieGenie! Please type your query below and press Enter to chat.")
        
        # Initialize chat log file if not present
        if not os.path.exists("chat_log.csv"):
            with open("chat_log.csv", "w", newline='', encoding='utf-8') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(['User Input', 'Chatbot Response', 'Timestamp'])

        counter += 1
        user_input = st.text_input("You", key=f"user_input_{counter}")

        if user_input:
            user_input_str = str(user_input).strip()
            response = foodiegenie_chatbot(user_input_str)
            st.text_area("FoodieGenie:", value=response, height=120, max_chars=None, key=f"chatbot_{counter}")

            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            with open('chat_log.csv', 'a', newline='', encoding='utf-8') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow([user_input_str, response, timestamp])

            if response.lower() in ['thank you for chatting with me!', 'goodbye', 'bye']:
                st.write("Thank you for interacting with FoodieGenie! Have a great day!")
                st.stop()

    # Conversation History
    elif choice == "Conversation History":
        st.header("Conversation History")
        if os.path.exists('chat_log.csv') and os.path.getsize('chat_log.csv') > 0:
            with open('chat_log.csv', 'r', encoding='utf-8') as csvfile:
                csv_reader = csv.reader(csvfile)
                next(csv_reader)  # Skip header row
                for row in csv_reader:
                    st.markdown(f"**User:** {row[0]}")
                    st.markdown(f"**FoodieGenie:** {row[1]}")
                    st.markdown(f"**Timestamp:** {row[2]}")
                    st.markdown("---")
        else:
            st.write("No conversation history found yet. Start chatting to create one!")

    # About
    elif choice == "About":
        st.write("Welcome to FoodieGenie Chatbot!")
        st.subheader("Project Overview:")
        st.write("""
            FoodieGenie is an AI-powered chatbot designed to enhance the guest experience in a 5-star hotel. 
            It handles dining orders, special requests, and provides general hotel information.
            Built using Python, Natural Language Processing (NLP), and the Logistic Regression algorithm, 
            FoodieGenie automates interactions to reduce response times and ensure 24/7 guest support.
        """)

        st.header("Intents and Features")
        st.write("Below are the intents the chatbot currently supports:")
        for intent in intents:
            st.markdown(f"- **{intent['tags']}**: {intent.get('description', 'No description provided.')}")
        
        st.header("Key Achievements")
        st.subheader("1. Guest Query Handling:")
        st.write("FoodieGenie effectively processes user queries related to hotel services and dining.")
        st.subheader("2. NLP Integration:")
        st.write("Utilizes NLP techniques to understand guest input and generate accurate responses.")
        st.subheader("3. Dining and Special Requests Automation:")
        st.write("Handles dining orders and special guest requests efficiently.")
        st.subheader("4. Streamlit Web Interface:")
        st.write("Provides an interactive interface for seamless guest interaction.")

        st.header("Future Scope")
        st.subheader("1. Advanced Intent Identification:")
        st.write("Improving intent recognition to better understand complex user queries.")
        st.subheader("2. Emotion and Sentiment Analysis:")
        st.write("Integrating emotion detection to provide empathetic responses to guests.")
        st.subheader("3. Multi-Language Support:")
        st.write("Adding support for multiple languages to cater to diverse guests.")
        st.subheader("4. Integration with Hotel Management Systems:")
        st.write("Connecting with existing hotel systems to automate service delivery.")

if __name__ == '__main__':
    main()
