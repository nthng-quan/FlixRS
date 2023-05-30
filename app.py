"""
Streamlit app
"""

import streamlit as st

st.set_page_config(page_title="FlixRS - Movies recommender system", page_icon="🔍", layout="wide")

with st.sidebar:
    st.header("🔍 FlixRS")
    st.write("A movies recommender system")

    st.header("📝 About")
    st.write("About...")

    st.header("🔧 Settings")
    st.slider("Number of movies", min_value=0, max_value=20, value=20, step=1)

    method=st.selectbox("Method", options=["CountVectorizer", "bert-base-nli-mean-tokens"])
    dist=st.selectbox("Distance", options=["Cosine similarity", "Euclidean distance"])


st.header("🔍 FlixIRS - FlixRS Recommender System for movies")
st.subheader("Movie Recommendation")
user_request = st.text_input("Anything...", value="")

if st.button("Search"):
    if user_request == "":
        st.write("Please enter something...")
    else:
        method
        dist
        st.write("Here are some movies you might like:")
        st.write(user_request)
        for i in range(5):
            st.write(f"{i+1}. Movie {i+1}")
else:
    st.write("No movies found.")
