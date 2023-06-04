# FlixRS - FlixRS Recommender System

## Introduction
FlixRS is an advanced recommender system designed to provide personalized movie recommendations to users based on the similarity between user requests and movie descriptions. Powered by sentence-transformer models, FlixRS leverages natural language processing (NLP) techniques and machine learning algorithms to accurately match user preferences with relevant movies. Additionally, FlixRS features an interactive chatbot, driven by the powerful GPT language model, which can answer user queries and provide detailed information about movies. By integrating with Yahoo search results, the chatbot ensures comprehensive and up-to-date movie insights.

## Technical Overview
- FlixRS combines cutting-edge NLP techniques and machine learning algorithms to deliver accurate movie recommendations. By encoding movie descriptions and user requests into semantic vectors using sentence-transformer models, FlixRS calculates the similarity score between them. This enables the system to generate a curated list of movie recommendations that align closely with the user's preferences.

- The chatbot component of FlixRS utilizes the GPT language model to provide an interactive and engaging experience. The chatbot can intelligently respond to user queries, offer insights about movies, and engage in conversational interactions. With the ability to integrate with Yahoo search results, the chatbot ensures users receive comprehensive and up-to-date information about movies, including reviews, ratings, release dates, and more.

## How to Install
To install and run FlixRS, follow these steps:

1. Install dependencies:
   ```
   pip install -r requirements.in
   ```
   or
   ```
   pip install -r requirements.txt
   ```

2. Launch the application using Streamlit:
   ```
   streamlit run app.py
   ```

Alternatively, you can use Docker to build and run the application:

```
docker build -t flixrs .
docker run -p 8501:8501 --gpus all flixrs 
```

## Usage
- Access FlixRS through the following public URL: https://flixrs.streamlit.app/. For the full functionality of the chatbot, an OpenAI API key is required.

- To test the system, you can use the provided API key:

    `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`.

- Once you access the application, you can interact with FlixRS in various ways. Input your movie preferences or specific queries to receive personalized movie recommendations or detailed information about movies. The chatbot component will provide responses based on the input, engaging in informative and interactive conversations.

- For enhanced movie information, the chatbot seamlessly integrates with Yahoo search results, enriching the content it provides. This integration ensures that users have access to comprehensive movie details, enabling them to make informed decisions about their movie choices.

Enjoy exploring new movies and engaging in informative conversations with the intelligent chatbot within FlixRS!