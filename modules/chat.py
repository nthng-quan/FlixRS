"""
    docstring
"""
import streamlit as st
from modules.utils import chatutils

# openai.api_key = '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'
def show_chat(movies_raw) -> None:
    """
    docstring
    """
    st.subheader("Here are your previous search results:")
    movies = movies_raw[
            ["title", "type", "description", "country", "director", "cast"]
        ].reset_index(drop=True)

    st.dataframe(movies)

    if st.session_state.openai is True:
        models = [model for model in st.session_state["model_list"] if "gpt" in model]
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
        )

        chatutils.chat(movies_raw, mv_chosen, models)
    else:
        st.error(
            "Enter your OpenAI API Key, check your api key at https://platform.openai.com/account/api-keys"
        )
