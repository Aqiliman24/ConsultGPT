from dotenv import load_dotenv
from random import choice
from flask import Flask,request,jsonify
import os
import openai

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

start_sequence = "\nDr Athira:"
restart_sequence = "\nYou:"
prompt = ""

def ask(question, chat_log=None):
    prompt_text = f'{chat_log}{restart_sequence}: {question}{start_sequence}:'
    response = openai.Completion.create(
    model="text-davinci-003",
    # model='gpt-3.5-turbo',
    prompt=prompt_text,
    temperature=0.15,
    max_tokens=300,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0.6
    )
    story = response['choices'][0]['text']
    return str(story)

def append_interaction_to_chat_log(question, answer, chat_log=None):
    if chat_log is None:
        chat_log = prompt
    return f'{chat_log}{restart_sequence} {question}{start_sequence}{answer}'