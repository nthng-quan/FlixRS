"""
Streamlit App for Movie Recommendations

This app allows users to search for movie recommendations based on their input.

"""

import streamlit as st
import model

# Set page configuration
st.set_page_config(
    page_title="FlixRS - Movies recommender system", page_icon="🔍", layout="wide"
)

with st.sidebar:
    # About section
    st.header("📝 About FlixRS")
    st.write(
        "Welcome to FlixRS, an NLP movie recommender system designed \
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
        options=["CountVectorizer", "bert-base-nli-mean-tokens", "all-MiniLM-L6-v2"],
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
        help="Choose to precalculate embeddings or not (for bert-base-nli-mean-tokens and all-MiniLM-L6-v2)",
    )
    dist = st.selectbox(
        "Distance",
        options=["Cosine similarity", "Euclidean distance"],
        help="Choose the distance metric to use for similarity calculation",
    )


# Main content section
st.header("🔍 FlixIRS - FlixRS Recommender System for movies")
st.subheader("Movie Recommendation")

# User input
user_request = st.text_input("Anything in your mind...", value="")

# Search button
if st.button("Search"):
    if user_request == "":
        st.write("Please enter something...")
    else:
        st.write("**Here are some movies you might like:**")
        try:
            movies = model.get_recommendations(
                user_request, device_, method, precalculation, dist, n_movies
            )
        except RuntimeError as esc:
            st.error(
                "RuntimeError: CUDA out of memory. Consider using CPU or CountVectorizer method."
            )
            raise RuntimeError from esc

        movies = movies[
            ["title", "description", "country", "director", "cast"]
        ].reset_index(drop=True)
        st.table(movies)
else:
    st.write("Enter something and press the search button...")
