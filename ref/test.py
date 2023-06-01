import openai
from search_engine_parser.core.engines.yahoo import Search as YahooSearch

# Set up your OpenAI API credentials
openai.api_key = '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'

# Define a function to generate a response from ChatGPT
def generate_response(prompt):
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=prompt,
        max_tokens=200,
        temperature=0.7,
        n=1,
        stop=None,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    return response.choices[0].text.strip()

# Define the search function
def search(query):
    results = []
    for i in range(1, 3):
        search_args = (query, i)
        ysearch = YahooSearch()
        yresults = ysearch.search(*search_args)

        for title, link, description in zip(yresults["titles"], yresults["links"], yresults["descriptions"]):
            results.append(f'TITLE: {title} LINK: {link} DESCRIPTIONS: {description}')

    return results

# Define a function to perform the search and generate a response from ChatGPT
def perform_search_and_generate_response(query):
    results = search(query)
    prompt = "ChatGPT: " + query.strip() + "\n"

    # Add search results to the prompt
    for result in results:
        prompt += result + "\n"

    # Generate a response from ChatGPT
    response = generate_response(prompt)

    # Print and display the response
    print(response)

# Start the conversation with ChatGPT
print("ChatGPT: Hello! How can I assist you today?")

# Enter the main interaction loop
while True:
    user_input = input("User: ")

    # Check if the user input is a search query
    if user_input.lower().startswith("search"):
        query = user_input[len("search"):].strip()
        perform_search_and_generate_response(query)
    else:
        # Add the user's input to the prompt
        prompt = "ChatGPT: " + user_input.strip() + "\n"

        # Generate a response from ChatGPT
        response = generate_response(prompt)

        # Print and display the response
        print(response)
