"""
Streamlit App for Movie Recommendations

This app allows users to search for movie recommendations based on their input.

"""

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

# # openai session_state variables
if 'openai' not in st.session_state:
    st.session_state['openai'] = False

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

    with st.expander(label="**🧐 How to use**", expanded=True):
        st.markdown(
            """
            - Just type anything in the search box. FlixRS will try its best
            and recommend you some movies based on your input.

            - Then you can chat with FlixRS Chatbot to get more information about the Movie/TV show.

            - You can playaround with the settings bellow to see how it affects the recommendations and chatbot response.

            - Documentation: [Github](https://github.com/nthng-quan/FlixRS)
            """
        )

    # Settings section
    st.header("⚙️ System configuration")
    with st.expander(label="**🔍 Recommender configuration**", expanded=False):
        n_movies = st.slider(
            "Number of movies",
            min_value=1,
            max_value=20,
            value=5,
            step=1,
            help="Choose the number of movies to recommend",
            key="n_movies"
        )

        method = st.selectbox(
            "Method/Model",
            options=[
                "all-MiniLM-L6-v2",
                "bert-base-nli-mean-tokens",
                "CountVectorizer",
            ],
            help="Choose the method/model to use for embedding calculation",
            key="method"
        )
        precalculation = st.radio(
            "Use precalculated embeddings",
            options=["True", "False"],
            help="Choose to precalculate embeddings or not\
                (only applied to bert-base-nli-mean-tokens and all-MiniLM-L6-v2)",
            key="precalculation",
        )
        device = st.radio(
            "Device",
            options=["cuda", "cpu"],
            help="Choose device to run the model on - to calculate embeddings (GPU or CPU)",
            key="device",
        )
        dist = st.selectbox(
            "Distance function",
            options=["Cosine similarity", "Euclidean distance"],
            help="Choose the distance metric to use for similarity calculation",
            key="dist",
        )
        
    with st.expander("**🤖 Chatbot configuration**"):
        api_key = st.text_input(
            label="🔑 API Key",
            placeholder="OpenAI API Key",
            # value="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",
            value="",
            type="password",
            help="Enter your OpenAI API Key, check your api key in https://platform.openai.com/account/api-keys",
            key="api_key",
            on_change=chatutils.check_openai_api_key,
        )
        if st.session_state.openai is True:
            st.write("⚙️ GPT Configuration")
            model_option = st.selectbox(
                "Select Model",
                st.session_state.model_list,
                help="Choose the model to use for generating text",
                key="model_option",
            )
            max_tokens = st.slider(
                "Max tokens",
                min_value=5,
                max_value=500,
                value=200,
                step=1,
                label_visibility="visible",
                help="The maximum number of tokens to be generated.",
                key="max_tokens",
            )
            temperature = st.slider(
                "Temperature",
                min_value=0.0,
                max_value=1.0,
                value=0.5,
                step=0.1,
                label_visibility="visible",
                help="Controls randomness. Lowering results in less random completions. As the temperature approaches zero, the model will become deterministic and repetitive. Higher temperature results in more random completions.",
                key="temperature",
            )
            search_intergrated = st.checkbox(
                "Yahoo search result integrated",
                value=False,
                help="Provide search results of chosen movie/TV show from Yahoo to chatbot for better response",
                key="search_intergrated"
            )
            if search_intergrated:
                n_results = st.slider(
                    "Max number of results",
                    min_value=1,
                    max_value=10,
                    value=5,
                    step=1,
                    help="Choose the number of results to return (use with caution, too many results may reach the API limit)",
                    key="n_results"
                )
            if st.button("Clear chat", use_container_width=True):
                chatutils.clear_chat()
                st.success("Chat cleared")

with tab1:
    # Main content section
    st.header("🔍 FlixRS - FlixRS Recommender System for movies")
    st.subheader("Movie Recommendation")

    # User input
    user_request = st.text_input(
        "Anything in your mind...",
        placeholder="Movie description...",
        value="A youthful opportunist achieves prosperity by roaming the roads of Los Angeles, documenting calamities and mortality. However, the shadows he captures begin to consume him."
    )

    # Search button
    if st.button("Search") or user_request != "":
        if user_request == "":
            st.write("Please enter something...")
        else:
            st.write("**Here are some movies you might like:**")
            try:
                movies_raw = model.get_recommendations(
                    user_request, device, method, precalculation, dist, n_movies
                ).reset_index(drop=True)
            except RuntimeError as esc:
                st.error(
                    "RuntimeError: CUDA out of memory. Consider using CPU or CountVectorizer method."
                )
                raise RuntimeError from esc

            movies = movies_raw[
                ["title", "description", "country", "director", "cast"]
            ].reset_index(drop=True)
            movies.index += 1

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
