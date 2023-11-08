import json
import openai
from django.conf import settings

openai.api_key = settings.OPENAI_API_KEY


def get_gpt_function():
    functions = [
        {
            "name": "get_monetizable_item_list",
            "description": "Returns a list of monetizable items from the provided text",
            "parameters": {
                "type": "object",
                "properties": {
                    "monetizable_items": {
                        "type": "string",
                        "description": "A comma seperated list of monetizable items from the provided text"
                    },
                }
            }
        },
        {
            "name": "get_business_type_list",
            "description": "Returns a list of related business categories according to the provided text",
            "parameters": {
                "type": "object",
                "properties": {
                    "business_types": {
                        "type": "string",
                        "description": "A comma seperated list of related business categories according to the "
                                       "provided text"
                    },
                }
            }
        },
        {
            "name": "get_top_companies_list",
            "description": "Returns a list of top companies in the provided business category",
            "parameters": {
                "type": "object",
                "properties": {
                    "top_companies": {
                        "type": "string",
                        "description": "A comma seperated list of top companies in the provided business category"
                    },
                }
            }
        },
        {
            "name": "get_contact_and_draft",
            "description": "Returns the contact information for the given company along with a draft email to the "
                           "given company",
            "parameters": {
                "type": "object",
                "properties": {
                    "contact_info": {
                        "type": "string",
                        "description": 'The contact information (website, email and phone(optional) ) for the '
                                       'provided company in the following format:'
                                       '{"contact_us_page": "www.example.com/contact-us"}'
                                       # '{"website": "www.example.com", '
                                       # '"email": "abc@example.com", "phone": "1234567890"}'
                    },
                    "draft": {
                        "type": "string",
                        "description": "Write a draft email to the selected company in the following format:"
                                       "(Insert name of company contact),I’m on the Harvard Lampoon’s Business "
                                       "board, we are the oldest humor magazine in the country. I have an article "
                                       "that {Summarize the article pasted} and it mentions services and products "
                                       "related to your business. We want to have a humorous, article specific, "
                                       "ad on our website. Would you be interested in working with us? Cheers,"
                    },
                }
            }
        },
    ]
    return functions


def get_monetizable_item_list(monetizable_items):
    monetizable_items = monetizable_items.split(",")
    return json.dumps({"monetizable_items": monetizable_items})


def gpt_turbo_model_request(prompt, function_id=0):
    # Function IDs:
    # 0: get_monetizable_item_list
    # 1: get_business_type_list
    # 2: get_top_companies_list
    # 3: get_contact_and_draft

    try:
        # prompt = (f"This is an article from the lampoon's website {article_content} "
        #           f"I want to have an advertisement on this page, "
        #           f"but I think it would be funny to make whoever the advertiser is be related to one of the "
        #           f"elements in the piece. What are some ideas of companies I could reach out to?")

        functions = get_gpt_function()

        # time.sleep(5)  # adding sleep of 5 seconds b/w each request to model

        response = openai.ChatCompletion.create(
            model=settings.GPT_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You are a useful business assistant."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            functions=functions,
            function_call={
                "name": functions[function_id]["name"]
            }
        )
        # Parsing the ChatGPT JSON response.
        arguments = response["choices"][0]["message"]["function_call"]["arguments"]
        if arguments:
            json_obj = json.loads(arguments)
            return json_obj
        else:
            return None
        pass
    except Exception as e:
        print(f"Error: {e}")
        return None


def gpt_functionless_request(prompt):
    try:

        response = openai.ChatCompletion.create(
            model=settings.GPT_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You are a useful business assistant."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
        )
        # Parsing the ChatGPT JSON response.
        # arguments = response["choices"][0]["message"]["function_call"]["arguments"]
        # if arguments:
        #     json_obj = json.loads(arguments)
        #     return json_obj
        # else:
        #     return None
        # pass
        response = response['choices'][0]['message']['content']
        return response
    except Exception as e:
        print(f"Error: {e}")
        return None
