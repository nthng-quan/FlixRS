"""
Streamlit App for Movie Recommendations

This app allows users to search for movie recommendations based on their input.

"""

import openai
import streamlit as st
from modules import chat
from modules import model

# Set page configuration
st.set_page_config(
    page_title="FlixRS - Movies recommender system",
    page_icon="🔥",
    initial_sidebar_state="expanded",
    layout="wide",
)

# session_state variables
st.session_state["openai"] = False

tab1, tab2 = st.tabs(["Recommender", "Chatbot"])

with st.sidebar:
    # About section
    st.header("📝 About FlixRS")
    st.write(
        "Welcome to FlixRS, an NLP-based movie recommender system designed \
        to help you discover your next favorite movies."
    )

    st.subheader("How to use")
    st.write(
        "Just type anything in the search box. FlixRS will try its best\
        and recommend you some movies based on your input."
    )

    # Settings section
    st.header("🔧 Settings")
    n_movies = st.slider(
        "Number of movies",
        min_value=0,
        max_value=20,
        value=5,
        step=1,
        help="Choose the number of movies to recommend",
    )

    method = st.selectbox(
        "Method/Model",
        options=["all-MiniLM-L6-v2", "bert-base-nli-mean-tokens", "CountVectorizer"],
        help="Choose the method/model to use for embedding calculation",
    )
    device_ = st.radio(
        "Device",
        options=["cuda", "cpu"],
        help="Choose device to run the model on (GPU or CPU)",
    )
    precalculation = st.radio(
        "Precalculated embeddings",
        options=["True", "False"],
        help="Choose to precalculate embeddings or not\
            (only applied to bert-base-nli-mean-tokens and all-MiniLM-L6-v2)",
    )
    dist = st.selectbox(
        "Distance function",
        options=["Cosine similarity", "Euclidean distance"],
        help="Choose the distance metric to use for similarity calculation",
    )
    api_key = st.text_input(
        label="API Key",
        placeholder="OpenAI API Key",
        value="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",
        type="password",
        help="Enter your OpenAI API Key, check your api key in https://platform.openai.com/account/api-keys",
    )

    if api_key:
        st.session_state["api_key"] = api_key
        openai.api_key = st.session_state["api_key"]
        try:
            st.session_state["model_list"] = [x.id for x in openai.Model.list().data]
            st.session_state["openai"] = True
            st.success("API Key is valid")
        except openai.error.AuthenticationError:
            st.session_state["openai"] = False
            st.error("Invalid API Key")

with tab1:
    # Main content section
    st.header("🔍 FlixRS - FlixRS Recommender System for movies")
    st.subheader("Movie Recommendation")

    # User input
    user_request = st.text_input(
        "Anything in your mind...", placeholder="Movie description...", value=""
    )

    # Search button
    if st.button("Search") or user_request != "":
        if user_request == "":
            st.write("Please enter something...")
        else:
            st.write("**Here are some movies you might like:**")
            try:
                movies_raw = model.get_recommendations(
                    user_request, device_, method, precalculation, dist, n_movies
                ).reset_index(drop=True)
            except RuntimeError as esc:
                st.error(
                    "RuntimeError: CUDA out of memory. Consider using CPU or CountVectorizer method."
                )
                raise RuntimeError from esc

            movies = movies_raw[
                ["title", "description", "country", "director", "cast"]
            ].reset_index(drop=True)

            st.table(movies)
    else:
        st.write("Enter something and press the search button...")

with tab2:
    st.header("🤖 FlixRS - FlixRS Chatbot")
    try:
        chat.show_chat(movies_raw)
    except NameError as esc:
        try:
            title = movies["title"]
        except NameError:
            st.write("Please search for some movies first...")
        else:
            st.write(f"Error occured {esc}")
