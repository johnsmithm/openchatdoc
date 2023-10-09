import openai
import json
import os
from embeddings.vector import get_context
from chat.prompts import PROMPT_SYSTEM, PROMPT_QUERY

openai.api_key = os.environ.get("OPENAI_API_KEY")

def generate_gpt_response(messages_list, model='gpt-3.5-turbo-16k-0613'):
    """Handle openai response."""
    completion = openai.ChatCompletion.create(
        model=model, 
        messages=messages_list)
    return completion.choices[0].message["content"]

def get_model_name():
    """get model name"""
    return os.environ.get("MODEL_NAME", 'gpt-3.5-turbo-16k-0613')

def get_response_llm(request_json):
    """get response from llm."""
    messages_list = request_json.get('message_list')
    query = request_json.get('query')

    model_name = get_model_name()

    context = get_context(query)

    messages_list  = [{"role": 'system', "content": PROMPT_SYSTEM}] + messages_list
    messages_list += [{"role": 'user', 
                       "content": PROMPT_QUERY.format(context=context, 
                                                      query=query)}]
    print(messages_list)
    return generate_gpt_response(messages_list, model_name)
