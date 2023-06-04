"""
    Displaying previous search results and initiating a chat with the ChatGPT chatbot.

    Functions:
    - show_chat(movies_raw): Displays previous search results and allows users to initiate a chat with the ChatGPT chatbot.

    Usage:
    - Ensure that an OpenAI API key is set to enable the chatbot functionality.
    - Enter the API key in the designated text input field.
    - Select a movie from the displayed search results to initiate a chat with the ChatGPT chatbot.
"""
import streamlit as st
from modules.utils import chatutils


def show_chat(movies_raw) -> None:
    """
    Display search results and enable chat with ChatGPT about a Movie/TV show.

    Parameters
    ----------
    movies_raw : pandas.DataFrame
        data containing information about the recommended movies/TV shows.
    """
    st.subheader("Here are your previous search results:")
    movies = movies_raw[
        ["title", "type", "description", "country", "director", "cast"]
    ].reset_index(drop=True)
    movies.index += 1

    st.dataframe(movies)

    if st.session_state.openai is True:
        # initialize session state
        if "generated" not in st.session_state:
            st.session_state["generated"] = []

        if "past" not in st.session_state:
            st.session_state["past"] = []

        st.subheader("💬 Chatting with ChatGPT about the Movie/TV show")
        mv_chosen = st.selectbox(
            label="Chat with ChatGPT for more infomation about this movie",
            options=movies,
            help="You can chat with ChatGPT to get more information about the Movie/TV show",
            label_visibility="collapsed",
            on_change=chatutils.clear_chat,
        )
        chatutils.chat(movies_raw, mv_chosen)
    else:
        st.error(
            "Enter your OpenAI API Key to enable the chatbot, check your api key at https://platform.openai.com/account/api-keys"
        )
        st.text_input(
            label="API Key",
            placeholder="OpenAI API Key",
            # value="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",
            value="",
            type="password",
            help="Enter your OpenAI API Key, check your api key in https://platform.openai.com/account/api-keys",
            key="api_key_opt",
            on_change=chatutils.check_openai_api_key,
            label_visibility="collapsed",
        )
