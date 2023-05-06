from .models import *
import openai, os
import json


def init(request): # stat conversation with gpt
    text = "I want you to act as my academic writing mentor and polish my essay according to my instructions."
    os.environ["http_proxy"] = "http://127.0.0.1:7890"
    os.environ["https_proxy"] = "http://127.0.0.1:7890"
    openai.api_key = "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"
    res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature=0.8,
        max_tokens=10000,
        messages=[
            {"role": "user", "content": f"{text}"}
        ]
    )



def chat(request): # chat with gpt
    text = request.POST.get('text')
    print(text)
    os.environ["http_proxy"] = "http://127.0.0.1:7890"
    os.environ["https_proxy"] = "http://127.0.0.1:7890"
    openai.api_key = "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"
    res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature=0.8,
        max_tokens=10000,
        messages=[
            {"role": "user", "content": f"{text}"}
        ]
    )

    response = res.choices[0].message["content"]
    print(response)

    chat = Chat.objects.create(
        text=text,
        gpt=response
    )
    chat.save() # store the input , answer given by gpt and time to the database

    


def respond(request): # get answer and return the answer with json form
    text = request.POST.get('text')
    print(text)
    os.environ["http_proxy"] = "http://127.0.0.1:7890"
    os.environ["https_proxy"] = "http://127.0.0.1:7890"
    openai.api_key = "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"
    res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature=0.8,
        max_tokens=10000,
        messages=[
            {"role": "user", "content": f"{text}"}
        ]
    )

    response = res.choices[0].message["content"]
    #print(response)
    length_of_answer=len(response)

    answer=json.dumps({'answer': response , 'start': 0, 'end': 7 , 'label':'FORM', 'len':length_of_answer}, sort_keys=True, indent=4, 
    separators=(',', ': '))
    return(answer)