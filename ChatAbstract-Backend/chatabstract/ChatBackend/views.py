from .models import *
import openai, os
import json
import re


def generate_prompt(operation) -> str:
    """generate prompts based on users' operations

    Args:
        operation (dict): a dict containing the user's operation in the following format
        operation = 
        {
            "text": "I eat food. I likes to eat food. I love hamburgers.",
            "start_index": 0,
            "end_index": 11,
            "comment": "Change to passive voice"
        }

    Returns:
        str: the prompt
    """
    prompt = "The original text is <" + operation["text"]+">. "
    sentence = operation["text"][operation["start_index"]:operation["end_index"]]
    prompt += "For sentence <" + sentence + ">, whose start index is " + str(operation["start_index"]) + " and end index is " + str(operation["end_index"]) + ", " + "the user's comment is " + operation["comment"] + "."
    prompt += "Notice only the sentence mentioned should be changed. Give me the changed version of the whole text, along with the changed part's start index and end index in the form of json, with three keys: text, start_index and end_index.  Your response should only contain json data. If the action is deletion, omit the start_index and end_index keys in your response."
    return prompt



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
    start = request.POST.get('start_index')
    end = request.POST.get('end_index')
    comment = request.POST.get('comment')
    operation = {
        "text": text,
        "start_index": start,
        "end_index": end,
        "comment": comment
    }
    prompt = generate_prompt(operation)
    #rint(text)
    os.environ["http_proxy"] = "http://127.0.0.1:12935"
    os.environ["https_proxy"] = "http://127.0.0.1:12935"
    openai.api_key = "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"
    res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature=0.8,
        max_tokens=10000,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    response = res.choices[0].message["content"]
    #print(response)
    #length_of_answer=len(response)
    #start_index=re.findall(r'"start_index": ([0-9]*?),', response)
    #end_index=re.findall(r'"end_index": ([0-9]*?),', response)
    #label=re.findall(r'"comment": (.*?),', response)

    #answer=json.dumps({'start': start_index, 'end': end_index , 'label':label}, sort_keys=True, indent=4, 
    #separators=(',', ': '))

    chat = Chat.objects.create(
        text=text,
        gpt=response
    )
    chat.save()

    op= Operation.objects.create(
        text=text,
        pos_start=start,
        pos_end=end,
        comment=comment
    )
    op.save()
    return(response)

