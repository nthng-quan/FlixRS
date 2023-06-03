"""
Streamlit App for Movie Recommendations

This app allows users to search for movie recommendations based on their input.

"""

import openai
import streamlit as st
from modules import chat
from modules.utils import chatutils
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
    st.header("📝 Welcome to FlixRS")
    st.markdown(
        """
        **An NLP-based movie recommender system designed
        to help you discover your next favorite movies.**
        """
    )

    st.subheader("How to use")
    st.markdown(
        """
        - Just type anything in the search box. FlixRS will try its best
        and recommend you some movies based on your input.

        - Then you can chat with FlixRS Chatbot to get more information about the Movie/TV show.
        """
    )

    # Settings section
    st.header("⚙️ System configuration")
    with st.expander(label="🔍 Recommender configuration", expanded=False):    
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
        
        # if st.session_state.openai is True:
        #     st.write("**Configuration**")
        #     model_option = st.selectbox(
        #         "Select Model",
        #         st.session_state.model_list,
        #         help="Choose the model to use for generating text",
        #     )
        #     max_tokens = st.slider(
        #         "Max tokens",
        #         min_value=5,
        #         max_value=500,
        #         value=200,
        #         step=1,
        #         label_visibility="visible",
        #         help="The maximum number of tokens to be generated."
        #     )
        #     temperature = st.slider(
        #         "Temperature",
        #         min_value=0.0,
        #         max_value=1.0,
        #         value=0.5,
        #         step=0.1,
        #         label_visibility="visible",
        #         help="Controls randomness. Lowering results in less random completions. As the temperature approaches zero, the model will become deterministic and repetitive. Higher temperature results in more random completions."
        #     )

    with st.expander("🤖 Chatbot configuration"):
        api_key = st.text_input(
            label="🔑 API Key",
            placeholder="OpenAI API Key",
            value="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",
            type="password",
            help="Enter your OpenAI API Key, check your api key in https://platform.openai.com/account/api-keys",
            key="api_key"
        )

        if api_key:
            openai.api_key = st.session_state["api_key"]
            try:
                st.session_state["model_list"] = [x.id for x in openai.Model.list().data]
                st.session_state["model_list"] = [model for model in st.session_state["model_list"] if "gpt" in model]
                st.session_state["openai"] = True
                # st.success("API Key is valid")
            except openai.error.AuthenticationError:
                st.session_state["openai"] = False
                st.error("Invalid API Key")
                
        if st.session_state.openai is True:
            st.write("⚙️ GPT Configuration")
            model_option = st.selectbox(
                "Select Model",
                st.session_state.model_list,
                help="Choose the model to use for generating text",
                key='model_option'
            )
            max_tokens = st.slider(
                "Max tokens",
                min_value=5,
                max_value=500,
                value=200,
                step=1,
                label_visibility="visible",
                help="The maximum number of tokens to be generated.",
                key='max_tokens'
            )
            temperature = st.slider(
                "Temperature",
                min_value=0.0,
                max_value=1.0,
                value=0.5,
                step=0.1,
                label_visibility="visible",
                help="Controls randomness. Lowering results in less random completions. As the temperature approaches zero, the model will become deterministic and repetitive. Higher temperature results in more random completions.",
                key='temperature'
            )
            if st.button("Clear chat", use_container_width=True):
                chatutils.clear_chat()
                messages=[]

                st.success("Chat cleared")

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
