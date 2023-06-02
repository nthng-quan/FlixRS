"""
    docstring
"""
import streamlit as st
import ref.chat

# openai.api_key = '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'
def chat(movies) -> None:
    """
    docstring
    """
    st.subheader("Here are your previous search results:")
    st.dataframe(movies)

    # movies = [f"{i+1}. {movie}" for i, movie in enumerate(movies["title"])]
    # if st.button("Chat"):
    if st.session_state.openai is True:
        # Define a function to generate a response from ChatGPT
        if "generated" not in st.session_state:
            st.session_state["generated"] = []

        if "past" not in st.session_state:
            st.session_state["past"] = []

        st.subheader("💬 Chatting with ChatGPT about the movie/TV series")
        mv_chosen = st.selectbox(
            label="Chat with ChatGPT for more infomation about this movie",
            options=movies,
            help="You can chat with ChatGPT to get more information about the movie",
            label_visibility="collapsed",
        )
        ref.chat.chatchat(mv_chosen)
    else:
        st.error(
            "Enter your OpenAI API Key, check your api key in https://platform.openai.com/account/api-keys"
        )
