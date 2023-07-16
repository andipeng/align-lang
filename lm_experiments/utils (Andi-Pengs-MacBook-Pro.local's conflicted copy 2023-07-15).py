import os
import openai
import time
import pandas as pd
import json
from tenacity import (
    retry,
    wait_random_exponential,
)

def openai_authenticate(azure=True):
    if azure:
        api_key_location=os.path.expanduser(os.path.join("~/.ssh/", "openai-azure"))
        api_base_location=os.path.expanduser(os.path.join("~/.ssh/", "openai-azure-base"))
        openai.api_type = "azure"
        openai.api_base = open(api_base_location).read().strip()
        openai.api_version = "2023-03-15-preview"
    else:
        # api_key_location=os.path.expanduser(os.path.join("~/.ssh/", "openai"))
        # openai.api_base = 'https://api.openai.com/v1'
        # openai.api_version = None
        openai.api_key = os.environ['OPENAI_API_KEY']
    # openai.api_key = open(api_key_location).read().strip()


@retry(wait=wait_random_exponential(min=1, max=60))
def openai_chatcompletion(messages, engine, temperature, azure, cache=None, cache_file=None):
    messages_cache_key = json.dumps(messages)
    if cache and messages_cache_key in cache:
        response = cache[messages_cache_key]
    else:
        if azure:
            response = openai.ChatCompletion.create(
                engine=engine,
                messages=messages,
                temperature=temperature,
            )
        else:
            response = openai.ChatCompletion.create(
                model=engine,
                messages=messages,
                temperature=temperature,
            )
        save_openai_cache({messages_cache_key: response}, cache, cache_file)
    choices = [dict(choice.items()) for choice in response["choices"]]
    return choices, response["created"]


@retry(wait=wait_random_exponential(min=1, max=60))
def openai_completion(prompt, engine, temperature, azure, cache=None, cache_file=None):
    if engine in ['gpt-4','gpt-4-32k','gpt-35-turbo','gpt-3.5-turbo']:
        return openai_chatcompletion(prompt, engine, temperature, azure, cache=cache, cache_file=cache_file)
    messages_cache_key = json.dumps(prompt)
    if cache and messages_cache_key in cache:
        response = cache[messages_cache_key]
    else:
        response = openai.Completion.create(
            engine=engine,
            prompt=prompt,
            temperature=temperature,
        )
        save_openai_cache({messages_cache_key: response}, cache, cache_file)
    choices = [dict(choice.items()) for choice in response["choices"]]
    return choices, response["created"]

def results2jsons():
    answer_jsons=[]
    for rule in range(11):
        df=pd.read_csv(f'results/gpt-4_rule-{rule}.csv')
        answer_json={}
        for group in ["object type", "object color"]:
            answer_json[group]=[v.split(' (')[0] for v in df[df.answer=='yes']['candidate'].values]
        answer_jsons.append(answer_json)
    return answer_jsons



def load_openai_cache(openai_cache_file):
    '''Loads the openai cache file into a dict.
    
    Args:
        openai_cache_file (str): The path to the openai cache file.
        
    Returns:
        dict: The openai cache dict.
    '''
    if not openai_cache_file:
        return None
    openai_cache = {}
    if os.path.exists(openai_cache_file):
        with open(openai_cache_file) as f:
            for line in f:
                openai_cache.update(json.loads(line))
    return openai_cache



def save_openai_cache(new_entry, openai_cache=None, openai_cache_file=None):
    '''Saves the new entry to the openai cache file and updates the openai_cache dict.
    
    Args:
        new_entry (dict): The new entry to save to the cache.
        openai_cache (dict): The openai cache dict to update.
        openai_cache_file (str): The path to the openai cache file.
    
    Returns:
        None
    '''
    if openai_cache_file:
        with open(openai_cache_file, "a") as wf:
            wf.write(json.dumps(new_entry)+"\n")
        openai_cache.update(new_entry)
