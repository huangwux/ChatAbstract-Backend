from .models import *
import openai, os
import json
import re


def init(request): # stat conversation with gpt
    text = "I want you to act as my academic writing mentor and polish my essay according to my instructions."
    os.environ["http_proxy"] = "http://127.0.0.1:12935"
    os.environ["https_proxy"] = "http://127.0.0.1:12935"
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
    os.environ["http_proxy"] = "http://127.0.0.1:12935"
    os.environ["https_proxy"] = "http://127.0.0.1:12935"
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

    

def respond_with_string(request): # get answer and return the answer with json form
    text = request.POST.get('text')
    print(text)
    os.environ["http_proxy"] = "http://127.0.0.1:12935"
    os.environ["https_proxy"] = "http://127.0.0.1:12935"
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
    #length_of_answer=len(response)
    chat = Chat.objects.create(
        text=text,
        gpt=response
    )
    chat.save()
    return(response)




def respond_with_json(request): # get answer and return the answer with json form
    text = request.POST.get('text')
    print(text)
    os.environ["http_proxy"] = "http://127.0.0.1:12935"
    os.environ["https_proxy"] = "http://127.0.0.1:12935"
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
    #length_of_answer=len(response)
    start_index=re.findall(r'"start_index": ([0-9]*?),', response)
    end_index=re.findall(r'"end_index": ([0-9]*?),', response)
    label=re.findall(r'"comment": (.*?),', response)

    answer=json.dumps({'start': start_index, 'end': end_index , 'label':label}, sort_keys=True, indent=4, 
    separators=(',', ': '))

    chat = Chat.objects.create(
        text=text,
        gpt=response
    )
    chat.save()
    return(answer)

def user_op(request): #store user's operation to database
    op_type=request.POST.get('type')
    op_pos_start=request.POST.get('pos_start')
    op_pos_end=request.POST.get('pos_end')
    op_content=request.POST.get('content')
    op=Operation.objects.create(
        type=op_type,
        pos_start=op_pos_start,
        pos_end= op_pos_end,
        content=op_content

    )
    op.save()
