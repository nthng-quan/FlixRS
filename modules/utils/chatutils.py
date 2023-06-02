"""
docstring
"""
import openai
import streamlit as st
from streamlit_chat import message
from modules import search

# TODO: clear on changing mv_chosen
def clear_chat() -> None:
    """
        docstring
    """
    for i in range(len(st.session_state["generated"]) - 1, -1, -1):
        st.session_state["generated"].pop(i)
        st.session_state["past"].pop(i)

def chat(movies, mv_chosen, models):
    """
        docstring
    """
    pd, column1, pd1, column2, pd2 = st.columns([0.05, 1.5, 0.05, 6, 0.05])
    with column1:
        st.write("**🔍 Search Configuration**")
        n_results = st.slider(
            "Number of results",
            min_value=1,
            max_value=20,
            value=5,
            step=1,
            help="Choose the number of results to return",
        )
        search_intergrated = st.checkbox(
            "Search integrated",
            value=False,
            help="Provide search results of chosen movie/TV show from Yahoo to chatbot",
        )

        background_prompt \
            = [f"INFORMATION FROM DATASET: {str(movies[movies['title'] == mv_chosen].to_dict(orient='records'))}"]
        if search_intergrated:
            background_prompt.append(f"YAHOO SEARCH: [{str(search.searcher(mv_chosen, n_results))}]")
        background_prompt = str(background_prompt)

        st.write("**⚙️ GPT Configuration**")
        model_option = st.selectbox("Select Model", models)
        max_tokens = st.slider(
            "Max words",
            min_value=5,
            max_value=500,
            value=200,
            step=1,
            label_visibility="visible",
        )
        temperature = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=2.0,
            value=0.5,
            step=0.1,
            label_visibility="visible",
        )

        if st.button("Clear chat"):
            clear_chat()
            messages=[]

            st.success("Chat cleared")

    with column2:
        running = False

        with st.form(key="my_form", clear_on_submit=True):
            user_input = st.text_input(f"Chat with GPT about **{mv_chosen}**", "", key="input", disabled=running)
            submit_button = st.form_submit_button(label='Send',use_container_width=True)

        sg1, sg2, sg3, sg4 = st.columns(4)
        with sg1:
            info=st.button("More information", key="suggest", use_container_width=True)
        with sg2:
            rating=st.button("Rating", key="rating", use_container_width=True)
        with sg3:
            cast=st.button("Cast", key="cast", use_container_width=True)
        with sg4:
            cont=st.button("Continue", key="continue", use_container_width=True)

        if info:
            user_input = "Tell me more about this movie/tv show"
            submit_button = True
        if rating:
            user_input = "What is the rating, IMDb rating,... of this movie/tv show"
            submit_button = True
        if cast:
            user_input = "Who are the cast and directors of this movie/tv show"
            submit_button = True
        if cont:
            user_input = "Continue"
            submit_button = True

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
                        max_tokens=max_tokens,
                        temperature=temperature,
                        top_p=1.0,
                        presence_penalty=0.0,
                        frequency_penalty=0.0,
                        stream=True,
                        messages=messages,
                        model=model_option
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
                