import copy
import random
import openai
import search as s
import time
import streamlit as st
from streamlit_tags import st_tags
import extra_streamlit_components as stx
from streamlit_chat import message

def chatchat(mv_chosen):
    openai.api_key = "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"
    # st.session_state.setdefault("logined", True)
    # st.session_state.setdefault("api_type", "open_ai")
    # st.session_state.setdefault("api_key", "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")
    # st.session_state.setdefault("model_list", ["gpt-3.5-turbo", "gpt-4", "gpt-4-32k"])
    # st.session_state.setdefault("model2deployment", {"gpt-3.5-turbo": "gpt-35-turbo"})
    # st.session_state.setdefault("model_name", "gpt-3.5-turbo")
    # st.session_state.setdefault("cost", 0.0)
    # st.session_state.setdefault("total_cost", 0.0)
    # st.session_state.setdefault("total_tokens", 0)
    # st.session_state.setdefault("generated", [])
    # st.session_state.setdefault("past", [])
    # st.session_state.setdefault("messages", [])

    # if "logined" not in st.session_state.keys() or not st.session_state["logined"]:
    #     st.error("Please login first")
    #     st.stop()

    if st.session_state.openai is True:
        models = ["gpt-3.5-turbo", "gpt-4", "gpt-4-32k"]
        models = [model for model in models if model in st.session_state["model_list"]]

    # if st.session_state["api_type"] == "azure":
    #     models = ["gpt-35-turbo", "gpt-4", "gpt-4-32k"]
    #     models = [
    #         model
    #         for model in models
    #         if model in st.session_state["model2deployment"].keys()
    #     ]

    if "generated" not in st.session_state:
        st.session_state["generated"] = []

    if "past" not in st.session_state:
        st.session_state["past"] = []

    c1, ce, c2, c3 = st.columns([1.5, 0.07, 6, 0.07])
    with c1:
        st.write("**⚙️ Configuration**")
        # background_prompt = st.text_area(
        #     "Background information",
        #     disabled=False,
        #     height=200,
        #     key="background_prompt",
        # )
        background_prompt = s.searcher(mv_chosen)
        model_option = st.selectbox("Select Model", models)
        max_tokens = st.slider(
            "Max words",
            min_value=5,
            max_value=500,
            value=100,
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
            # st.session_state["generated"] = []
            # st.session_state["past"] = []
            # st.session_state["messages"] = []
            for i in range(len(st.session_state["generated"]) - 1, -1, -1):
                st.session_state["generated"].pop(i)
                st.session_state["past"].pop(i)

            st.success("Chat cleared")

    with c2:
        # st.subheader("Chat", anchor=None)
        running = False
        if st.session_state.clear is False:
            running = True

        with st.form(key="my_form", clear_on_submit=True):
            user_input = st.text_input(f"Chat with GPT about **{mv_chosen}**", "", key="input", disabled=running)
            submit_button = st.form_submit_button(label='Submit')

        if submit_button:
            if user_input:
                background_prompt = '\n'.join(background_prompt)
                messages = [{"role": "system", "content": background_prompt}]
                for i in range(len(st.session_state["generated"])):
                    messages.append({"role": "user", "content": st.session_state["past"][i]})
                    messages.append({"role": "assistant", "content": st.session_state["generated"][i]})
                messages.append({"role": "user", "content": user_input})

                running = True
                if st.session_state.openai is True:
                    res = openai.ChatCompletion.create(
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
                    # key = len(st.session_state["generated"])
                    # message(user_input, avatar_style="pixel-art", key=str(key) + "_user", is_user=True)
                    for x in res:
                        if "content" in x.choices[0].delta.keys():
                            result += x.choices[0].delta.content
                    # message(result, avatar_style="pixel-art", key=str(key))

                st.session_state.past.append(user_input)
                st.session_state.generated.append(result)

            if st.session_state["generated"]:
                for i in range(len(st.session_state["generated"]) - 1, -1, -1):
                    message(st.session_state["generated"][i], key=str(i))
                    message(st.session_state["past"][i], is_user=True, key=str(i) + "_user")