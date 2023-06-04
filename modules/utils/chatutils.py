""" Chat utils

    Functions:
    - random_request():
        Generates a random request for the chatbot.
    - check_openai_api_key():
        Checks the OpenAI API key and sets up the required configurations.
    - clear_chat():
        Clears the chat history.
    - generate_background_prompt(movies, mv_chosen):
        Generates a background prompt for the chatbot based on the chosen movie.
    - chat(movies, mv_chosen):
        Initiates a chat with the chatbot, allowing users to interact and receive responses.

    The chatbot interacts with users using the Streamlit library and utilizes OpenAI GPT models for generating responses.
"""

import random
import openai
import streamlit as st
from streamlit_chat import message
from modules import search


def random_request() -> None:
    """
    Randomly selects a movie request and sets it as the user request in the session state.

    This function selects a random movie description from a predefined list of requests
    and sets it as the value for the 'user_request' key in the session state.

    Returns:
        update user_request in session state
    """
    requests = [
        "A youthful opportunist achieves prosperity by roaming the roads of Los Angeles, documenting calamities and mortality. However, the shadows he captures begin to consume him.",  # Nightcrawler
        "A chemistry teacher in high school who is suffering from cancer joins forces with a former student to ensure his family's financial stability by producing and selling crystallized methamphetamine.",  # Breaking Bad
        "Immersed in a captivating drama, this series delves into the inception of a captivating bond between an FBI criminal profiler and a sinister cannibalistic murderer",  # Hannibal
        "A mutated individual who hunts monsters for a living embarks on a fateful journey towards his ultimate fate.",  # The Witcher
        "spaceship, explosion, future",  # ...
    ]

    st.session_state["user_request"] = random.choice(requests)


def check_openai_api_key():
    """
    Checks the OpenAI API key and sets the session state variables.

    'api_key_opt' where user can enter the openAI key in chatbot tab (while 'api_key' is the one
    in Chatbot configuration)

    If 'api_key_opt' is not empty, it sets the value as the API key and clears 'api_key_opt'.
    Then, it sets the OpenAI API key and retrieves the list of available models.
    It filters the models to keep only those with 'gpt' in their ID and stores them in 'model_list'.
    Finally, it sets the 'openai' flag in the session state.

    Raises:
        openai.error.AuthenticationError: If an invalid API key is provided.

    Returns:
        None
    """
    # Check if 'api_key_opt' is provided and set it as the API key
    if st.session_state["api_key_opt"] != "":
        st.session_state["api_key"] = st.session_state["api_key_opt"]
        st.session_state["api_key_opt"] = ""

    # Set the OpenAI API key
    openai.api_key = st.session_state["api_key"]

    try:
        # Retrieve the list of available models
        model_list = [x.id for x in openai.Model.list().data]

        # Filter the models to keep only those with 'gpt' in their ID
        st.session_state["model_list"] = [
            model for model in model_list if "gpt" in model
        ]

        # Set the 'openai' flag to indicate a valid API key
        st.session_state["openai"] = True

    except openai.error.AuthenticationError:
        # If an AuthenticationError occurs, set the 'openai' flag to False and display an error message
        st.session_state["openai"] = False
        st.error("Invalid API Key")


def clear_chat() -> None:
    """
    Clears the chat history by removing all generated and past messages.

    It iterates over the generated and past messages lists in reverse order
    and removes each element using the 'pop()' function.

    Returns:
        None
    """
    # Iterate over the generated and past messages in reverse order
    for i in range(len(st.session_state["generated"]) - 1, -1, -1):
        # Remove the current generated message
        st.session_state["generated"].pop(i)
        # Remove the corresponding past message
        st.session_state["past"].pop(i)


def generate_background_prompt(movies, mv_chosen):
    """
    Generates the background prompt for the chatbot.

    It creates a list containing information from the dataset about the chosen movie.
    If the search integration is enabled, it also appends the search results from Yahoo (modules/search.py).

    Parameters:
        movies (pandas.DataFrame): The dataset containing movie information.
        mv_chosen (str): The chosen movie.

    Returns:
        str: The generated background prompt.
    """
    # Generate the information from the dataset
    background_prompt = [
        f"INFORMATION FROM DATASET: {str(movies[movies['title'] == mv_chosen].to_dict(orient='records'))}"
    ]

    # Check if search integration is enabled
    if st.session_state.search_intergrated:
        n_results = st.session_state.n_results
        # Append the Yahoo search results
        background_prompt.append(
            f"YAHOO SEARCH: [{str(search.searcher(mv_chosen, n_results, n_pages=1, only_description=True))}]"
        )

    # Convert the background prompt to a string
    background_prompt = str(background_prompt)

    return background_prompt


def chat(movies, mv_chosen):
    """
    Initiates a chat with the chatbot.

    Parameters:
        movies (pandas.DataFrame): The dataset containing movie information.
        mv_chosen (str): The chosen movie.
    """
    # User request for chatbot
    running = False
    with st.form(key="my_form", clear_on_submit=True):
        user_input = st.text_input(
            f"Chat with GPT about **{mv_chosen}**",
            "",
            key="input",
            disabled=running,
            help="It's optimal to clear the chat before chatting with another movie",
        )
        submit_button = st.form_submit_button(label="Send", use_container_width=True)

    # User request suggestions
    with st.container():
        sg1, sg2, sg3, sg4 = st.columns(4)
        info = sg1.button("More information", use_container_width=True)
        rating = sg2.button("Rating", use_container_width=True)
        cast = sg3.button("Cast", use_container_width=True)
        cont = sg4.button("Continue", use_container_width=True)

        if info:
            user_input = f"Tell me more about {mv_chosen}"
            submit_button = True
        if rating:
            user_input = f"What is the rating, IMDb rating,... of {mv_chosen}"
            submit_button = True
        if cast:
            user_input = f"Who are the cast and directors of {mv_chosen}"
            submit_button = True
        if cont:
            user_input = "Continue"
            submit_button = True

    # Background prompt
    background_prompt = generate_background_prompt(movies, mv_chosen)

    # Chatbot response
    if submit_button is True and user_input != "":
        with st.spinner("Thinking..."):
            messages = [{"role": "system", "content": background_prompt}]
            for i in range(len(st.session_state["generated"])):
                messages.append(
                    {"role": "user", "content": st.session_state["past"][i]}
                )
                messages.append(
                    {"role": "assistant", "content": st.session_state["generated"][i]}
                )
            messages.append({"role": "user", "content": user_input})

            running = True
            if st.session_state.openai is True:
                configs = openai.ChatCompletion.create(
                    max_tokens=st.session_state.max_tokens,
                    temperature=st.session_state.temperature,
                    top_p=1.0,
                    presence_penalty=0.0,
                    frequency_penalty=0.0,
                    stream=True,
                    messages=messages,
                    model=st.session_state.model_option,
                )
            result = ""
            with st.empty():
                for config in configs:
                    if "content" in config.choices[0].delta.keys():
                        result += config.choices[0].delta.content

            st.session_state.past.append(user_input)
            st.session_state.generated.append(result)

    if st.session_state["generated"]:
        # Display chat history
        for i in range(len(st.session_state["generated"]) - 1, -1, -1):
            message(st.session_state["generated"][i], key=str(i))
            message(st.session_state["past"][i], is_user=True, key=str(i) + "_user")
