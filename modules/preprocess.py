""" Preprocessing Module

This module provides functions for preprocessing the data.
"""

import pandas as pd


def preprocess(filename="data/netflix_titles_raw.csv"):
    """
    This function is used to preprocess the data.

    Parameters:
        filename (str): The filename of the raw data.

    Returns:
        None

    Steps:
        1. Drop 'duration' and 'date_added' columns.
        2. Fill missing values with 'UnKnown' for 'director', 'country', and 'cast' columns.
        3. Drop rows with missing values.
        4. Save the cleaned data to a CSV file.
    """
    data = pd.read_csv(f"{filename}.csv")

    # Drop 'duration' and 'date_added' columns
    data.drop(["duration", "date_added"], axis=1, inplace=True)

    # Fill missing values with 'UnKnown'
    data["director"] = data["director"].fillna("UnKnown")
    data["country"] = data["country"].fillna("UnKnown")
    data["cast"] = data["cast"].fillna("UnKnown")

    # Drop rows with missing values
    data.dropna(inplace=True)

    # Save to CSV
    data.to_csv(f"{filename}_clean.csv", index=False)
