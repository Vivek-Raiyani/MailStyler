from openai import OpenAI
import streamlit as st
client = OpenAI(api_key=st.secrets['api_keys']['api_key'])

def html_parse(content):
    html_content=content.split("html",maxsplit=1)
    html_content=html_content[1]
    html_content=html_content.split("```")
    print(html_content[0])
    return html_content[0]


def llm_call(query , messages_history):
    prompt={"role": "user", "content": f"{query}"}
    messages_history.append(prompt)
    print(messages_history)

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages_history
    )

    #print(completion.choices[0].message.content)
    content=html_parse(completion.choices[0].message.content)
    messages_history.append({
        "role" : "assistant",
        "content" : content
    })    
    print(messages_history)
    return content,messages_history
