import streamlit as st
from groq import Groq


def initialize_groq_client(api_key):
    try:
        return Groq(api_key=api_key)
    except Exception as e:
        st.error(f"Error initializing Groq client: {e}")
        return None

def get_wine_notes(client, wine_name, region, variety):
    system_prompt = f"""
    You are an AI assistant specialized in wine. Your task is to provide detailed tasting notes for wines based on their name, region, and variety.
    The user will provide the wine name, region, and variety, and you should generate descriptive tasting notes.
    """

    user_input = f"Wine Name: {wine_name}\nRegion: {region}\nVariety: {variety}\nPlease provide tasting notes ."
    
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ],
            model="llama3-70b-8192",  
            temperature=0.7  
        )
        response = chat_completion.choices[0].message.content
        return response.strip()
    except Exception as e:
        st.error(f"Error fetching wine notes: {e}")
        return "An error occurred while fetching the notes."


def main():
    st.set_page_config(page_title="Wine Notes Chatbot", page_icon="🍷")

    st.title("Wine Notes Chatbot 🍷")


    client_groq = initialize_groq_client("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")
    if client_groq is None:
        st.error("Failed to initialize the Groq client. Please check your API key.")
        return


    wine_name = st.text_input("Enter the wine name:")
    region = st.text_input("Enter the region:")
    variety = st.text_input("Enter the variety:")

    if st.button("Get Wine Notes"):
        if wine_name and region and variety:
            notes = get_wine_notes(client_groq, wine_name, region, variety)
            st.success(notes)
        else:
            st.error("Please fill in all the fields.")

if __name__ == "__main__":
    main()
