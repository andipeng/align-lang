import os
import openai
import time


def openai_authenticate(azure=True):
    if azure:
        api_key_location=os.path.expanduser(os.path.join("~/.ssh/", "openai-azure"))
        api_base_location=os.path.expanduser(os.path.join("~/.ssh/", "openai-azure-base"))
        openai.api_type = "azure"
        openai.api_base = open(api_base_location).read().strip()
        openai.api_version = "2023-03-15-preview"
    else:
        api_key_location=os.path.expanduser(os.path.join("~/.ssh/", "openai"))
        # openai.api_base = 'https://api.openai.com/v1'
        # openai.api_version = None
    openai.api_key = open(api_key_location).read().strip()
    
    
    
def openai_chatcompletion(messages, engine, temperature, azure):
    response=False
    i=0
    while not response:
        i+=1
        try:
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
        except Exception as e:
            if i>=10:
                return False, False
            if i>=5:
                print(f'Attempt {i} failed: {e}')
            elif i>=3: print(f'Attempt {i} failed.')
            time.sleep(5)
    choices = [dict(choice.items()) for choice in response.choices]
    return choices, response.created


def openai_completion(prompt, engine, temperature, azure):
    if engine in ['gpt-4','gpt-4-32k','gpt-35-turbo','gpt-3.5-turbo']:
        return openai_chatcompletion(prompt, engine, temperature, azure)
    response=False
    i=0
    while not response:
        i+=1
        try:
            response = openai.Completion.create(
                engine=engine,
                prompt=prompt,
                temperature=temperature,
            )
        except Exception as e:
            if i>=10:
                return False, False
            if i>=5:
                print(f'Attempt {i} failed: {e}')
            elif i>=3: print(f'Attempt {i} failed.')
            time.sleep(5)
    choices = [dict(choice.items()) for choice in response.choices]
    return choices, response.created