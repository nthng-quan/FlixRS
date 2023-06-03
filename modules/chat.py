"""
header docstring
"""
import streamlit as st
from modules.utils import chatutils

def show_chat(movies_raw) -> None:
    """
    docstring
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
            on_change=chatutils.clear_chat
        )
        chatutils.chat(movies_raw, mv_chosen)
    else:
        st.write("🔑 API Key")
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
