"""
    This file contains the model for movie recommendations based on sentence embeddings.

    It provides functions to get movie embeddings from descriptions and to generate recommendations
    based on user requests.
"""

import time
import numpy as np
import pandas as pd
import streamlit as st

import torch

from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import CountVectorizer

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import euclidean_distances
import preprocess

try:
    data = pd.read_csv("data/netflix_titles_clean.csv")
except FileNotFoundError:
    preprocess.preprocess("data/netflix_titles")
    data = pd.read_csv("data/netflix_titles_clean.csv")


def get_embeddings(device_, method="all-MiniLM-L6-v2", precalculation="True"):
    """
    This function is used to get the embeddings of the movie descriptions.

    Parameters:
        device_ (str): The device to use for embedding calculation
            ('cuda' or 'cpu').
        method (str, optional): The method to use for embedding calculation
            (default: "all-MiniLM-L6-v2").
        precalculation (str, optional): Whether to use precalculated embeddings
            or calculate them on the fly (default: "True").

    Returns:
        numpy.ndarray: The movie description embeddings.

    """
    if device_ == "cuda":
        if torch.cuda.is_available():
            device_ = "cuda"
        else:
            # Warning message when CUDA is not available
            st.warning(
                "CUDA not found, using CPU or consider using precalculated embeddings",
                icon="⚠️",
            )
            device_ = "cpu"

    if method == "CountVectorizer":
        # Using CountVectorizer method
        count = CountVectorizer(stop_words="english")
        count_matrix = count.fit_transform(data["description"])
        return count_matrix

    model = SentenceTransformer(method, device=device_)

    if precalculation == "True":
        try:
            # Attempt to load precalculated embeddings
            sentence_embeddings = np.load(f"data/movie_descriptions_{method}.npy")
        except FileNotFoundError:
            # Warning message when precalculated embeddings are not found
            st.warning(
                "Precalculated embeddings not found, calculating embeddings", icon="⚠️"
            )
            with st.spinner("Calculating embeddings..."):
                start_time = time.time()
                sentence_embeddings = model.encode(data["description"].values)
                np.save(f"data/movie_descriptions_{method}.npy", sentence_embeddings)
                end_time = time.time()
                elapsed_time = end_time - start_time
                st.success(
                    f"Done! Elapsed Time: {elapsed_time:.2f} seconds using {device_}"
                )
    else:
        # Calculate embeddings on the fly
        with st.spinner("Calculating embeddings..."):
            start_time = time.time()
            sentence_embeddings = model.encode(data["description"].values)
            np.save(f"data/movie_descriptions_{method}.npy", sentence_embeddings)
            end_time = time.time()
            elapsed_time = end_time - start_time
            st.success(
                f"Done! Elapsed Time: {elapsed_time:.2f} seconds using {device_}"
            )

    return sentence_embeddings


def get_recommendations(
    user_request,
    device_,
    method="all-MiniLM-L6-v2",
    precalculation="True",
    dist="Cosine similarity",
    n_movies=10,
):
    """
    This function is used to get the recommendations based on the user request.

    Parameters:
        user_request (str): The user's request or query.
        device_ (str): The device to use for embedding calculation ('cuda' or 'cpu').
        method (str, optional): The method to use for embedding calculation
            (default: "all-MiniLM-L6-v2").
        precalculation (str, optional): Whether to use precalculated embeddings
            or calculate them on the fly (default: "True").
        dist (str, optional): The distance metric to use for similarity
            calculation ("Cosine similarity" or "Euclidean distance", default: "Cosine similarity").
        n_movies (int, optional): The number of movies to recommend (default: 5).

    Returns:
        pandas.DataFrame: The recommended movies based on the user request.

    """
    if device_ == "cuda":
        if torch.cuda.is_available():
            device_ = "cuda"
        else:
            # Warning message when CUDA is not available
            st.warning("CUDA not found, using CPU", icon="⚠️")
            device_ = "cpu"

    if method == "CountVectorizer":
        # Using CountVectorizer method
        count = CountVectorizer(stop_words="english")
        sentence_embeddings = count.fit_transform(data["description"])
        request_embeddings = count.transform([user_request])
    else:
        model = SentenceTransformer(method, device=device_)
        request_embeddings = [model.encode(user_request)]
        sentence_embeddings = get_embeddings(device_, method, precalculation)

    if dist == "Cosine similarity":
        dist = cosine_similarity(request_embeddings, sentence_embeddings)
    else:
        dist = euclidean_distances(request_embeddings, sentence_embeddings)

    indices = np.argsort(dist[0])[::-1][:n_movies]
    return data.iloc[indices]
