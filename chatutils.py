import openai
import streamlit as st


# openai.api_key = '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'
def chat(movies) -> None:
    movies = [f"{i+1}. {movie}" for i, movie in enumerate(movies["title"])]
    st.subheader("Here your previous search results:")
    # if st.button("Chat"):
    if st.session_state.openai == True:
        # Define a function to generate a response from ChatGPT
        if "generated" not in st.session_state:
            st.session_state["generated"] = []

        if "past" not in st.session_state:
            st.session_state["past"] = []

        ce, c1, ce, c2, c3 = st.columns([0.001, 1.5, 0.07, 6, 0.07])
        with c1:
            st.subheader("Configuration", anchor=None)
            background_prompt = st.text_area(
                "Background information",
                disabled=False,
                height=100,
                key="background_prompt",
            )
            # model_option = st.selectbox("Select Model", models)
            max_tokens = st.slider(
                "Max words",
                min_value=5,
                max_value=4000,
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
        with c2:
            mv_chosen = st.selectbox(
                "Chat with ChatGPT for more infomation about this movie",
                options=movies,
                help="You can chat with GPT to get more information about the movie",
            )
            if st.button("Chat"):
                # TODO add chat
                st.write(
                    f"Chat with GPT for more infomation about the movie {mv_chosen} {st.session_state.openai}"
                )
    else:
        st.error(
            "Enter your OpenAI API Key, check your api key in https://platform.openai.com/account/api-keys"
        )
