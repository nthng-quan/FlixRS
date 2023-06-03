"""
header docstring
"""
import random
import openai
import streamlit as st
from streamlit_chat import message
from modules import search

def random_request() -> None:
    """
        docstring
    """
    requests = [
        "A youthful opportunist achieves prosperity by roaming the roads of Los Angeles, documenting calamities and mortality. However, the shadows he captures begin to consume him.", # Nightcrawler
        "A chemistry teacher in high school who is suffering from cancer joins forces with a former student to ensure his family's financial stability by producing and selling crystallized methamphetamine.", # Breaking Bad
        "Immersed in a captivating drama, this series delves into the inception of a captivating bond between an FBI criminal profiler and a sinister cannibalistic murderer", # Hannibal
        "A mutated individual who hunts monsters for a living embarks on a fateful journey towards his ultimate fate.", # The Witcher
        "spaceship, explosion, future" # ...
    ]   

    st.session_state['user_request']=random.choice(requests)

def check_openai_api_key():
    """
        docstring
    """
    if st.session_state["api_key_opt"] != "":
        st.session_state["api_key"] = st.session_state["api_key_opt"]
        st.session_state["api_key_opt"] = ""  
    openai.api_key = st.session_state["api_key"]
    try:
        model_list = [
            x.id for x in openai.Model.list().data
        ]
        st.session_state["model_list"] = [
            model for model in model_list if "gpt" in model
        ]
        st.session_state["openai"] = True

    except openai.error.AuthenticationError:
        st.session_state["openai"] = False
        st.error("Invalid API Key")

def clear_chat() -> None:
    """
        docstring
    """
    for i in range(len(st.session_state["generated"]) - 1, -1, -1):
        st.session_state["generated"].pop(i)
        st.session_state["past"].pop(i)

def generate_background_prompt(movies, mv_chosen):
    """
        docstring
    """
    background_prompt\
        = [f"INFORMATION FROM DATASET: {str(movies[movies['title'] == mv_chosen].to_dict(orient='records'))}"]
    if st.session_state.search_intergrated:
        n_results = st.session_state.n_results
        background_prompt.append(\
            f"YAHOO SEARCH: [{str(search.searcher(mv_chosen, n_results, n_pages=1, only_description=True))}]") 
    background_prompt = str(background_prompt)

    return background_prompt

def chat(movies, mv_chosen):
    """
        docstring
    """
    # user request for chatbot
    running = False
    with st.form(key="my_form", clear_on_submit=True):
        user_input = st.text_input(
            f"Chat with GPT about **{mv_chosen}**", "",
            key="input", disabled=running,
            help="Its optimal to clear the chat before chatting with another movie")
        submit_button = st.form_submit_button(label='Send', use_container_width=True)

    # user request suggestions
    with st.container():
        sg1, sg2, sg3, sg4 = st.columns(4)
        info\
            = sg1.button("More information", use_container_width=True)
        rating\
            = sg2.button("Rating", use_container_width=True)
        cast\
            = sg3.button("Cast", use_container_width=True)
        cont\
            = sg4.button("Continue", use_container_width=True)

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
        
    # background prompt
    background_prompt = generate_background_prompt(movies, mv_chosen)

    # chatbot response
    if submit_button is True and user_input != "":
        with st.spinner("Thinking..."):
            messages = [{"role": "system", "content": background_prompt}]
            for i in range(len(st.session_state["generated"])):
                messages.append({"role": "user", "content": st.session_state["past"][i]})
                messages.append({"role": "assistant", "content": st.session_state["generated"][i]})
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
                    model=st.session_state.model_option
                )
            result = ""
            with st.empty():
                for config in configs:
                    if "content" in config.choices[0].delta.keys():
                        result += config.choices[0].delta.content

            st.session_state.past.append(user_input)
            st.session_state.generated.append(result)

    if st.session_state["generated"]:
        for i in range(len(st.session_state["generated"]) - 1, -1, -1):
            message(st.session_state["generated"][i], key=str(i))
            message(st.session_state["past"][i], is_user=True, key=str(i) + "_user")
