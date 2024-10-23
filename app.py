import streamlit as st
from groq import Groq

def initialize_groq_client(api_key):
    try:
        return Groq(api_key=api_key)
    except Exception as e:
        st.error(f"Error initializing Groq client: {e}")
        return None

def get_wine_details(client, user_query):
    system_prompt = """
    You are an AI assistant specialized in wine. The user will ask you questions or provide a description of a wine, 
    and you should provide detailed tasting notes, quality assessment, region of origin, acidity, alcohol percentage, 
    year of production, rating, cost, and complementary food pairings.
    
    Answer in a conversational style, covering the tasting notes, wine's quality, where it comes from, acidity, 
    alcohol percentage, the year it was made, and rating out of 100. Also include an estimated price and a few 
    food pairings that would go well with it. 
    """

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_query}
            ],
            model="llama3-70b-8192",  
            temperature=0.7  
        )
        response = chat_completion.choices[0].message.content
        return response.strip()
    except Exception as e:
        st.error(f"Error fetching wine details: {e}")
        return "An error occurred while fetching the wine details."

def main():
    st.set_page_config(page_title="Wine Expert Chatbot", page_icon="🍷")

    st.title("Wine Expert Chatbot 🍷")

    # Initialize the Groq client
    client_groq = initialize_groq_client("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")
    if client_groq is None:
        st.error("Failed to initialize the Groq client. Please check your API key.")
        return

    # Single text input for natural language query
    user_query = st.text_area("Ask about a wine:", placeholder="Describe the wine or ask for details like tasting notes, region of origin, acidity, etc.")

    if st.button("Get Wine Details"):
        if user_query:
            details = get_wine_details(client_groq, user_query)
            st.success(details)
        else:
            st.error("Please enter a wine query.")

if __name__ == "__main__":
    main()
