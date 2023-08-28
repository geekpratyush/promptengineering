import openai
import streamlit as st
from IPython.display import display, HTML
import json
import panel as pn
pn.extension()

def get_completion(prompt, model="gpt-3.5-turbo",temperature="0.7"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]
def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]

def collect_messages(_):
    prompt = inp.value_input
    inp.value = ''
    context.append({'role':'user', 'content':f"{prompt}"})
    response = get_completion_from_messages(context) 
    context.append({'role':'assistant', 'content':f"{response}"})
    panels.append(
        pn.Row('User:', pn.pane.Markdown(prompt, width=600)))
    panels.append(
        pn.Row('Assistant:', pn.pane.Markdown(response, width=600, style={'background-color': '#F6F6F6'})))
 
    return pn.Column(*panels)


st.header('A Prompt Engineering Playground form :blue[Pratyush Ranjan Mishra] :sunglasses:')
with st.sidebar:
    st.title('🤖💬 Prompt Practice Bot :flag-in:')
    temp = st.slider('Acuracy temperature 0 being more acurate and 1 being more creative', 0.0, 1.0, 0.7)
    if 'OPENAI_API_KEY' in st.secrets:
        st.success('API key already provided!', icon='✅')
        openai.api_key = st.secrets['OPENAI_API_KEY']
    else:
        openai.api_key = st.text_input('Enter OpenAI API token:', type='password')
        if not (openai.api_key.startswith('sk-') and len(openai.api_key)==51):
            st.warning('Please enter your credentials!', icon='⚠️')
        else:
            st.success('Proceed to entering your prompt message!', icon='👉')




messages=[]

with st.expander("Exercise 01"):
    sys_message= {"role": "system", "content": st.text_area("System Message to Chatbot","You are an assistant that speaks like Shakespeare.")}
    usr_message={"role": "user", "content": st.text_area("User Message to Chatbot","Tell me a joke.")}
    #asst_message={"role": "assistant", "content": st.text_area("Assiststant message to Chatbot","Why did the chicken cross the road?")}
    #usr1_message={"role": "user", "content": st.text_area("User Message to Chatbot","I don't know.")}

    messages.insert(0,sys_message)
    messages.insert(1,usr_message)
    #messages.insert(2,asst_message)
    #messages.insert(3,usr1_message)
    #st.write(messages)
    if st.button("Process"):
        response = get_completion_from_messages(messages, temperature=temp)
        st.write(response)
with st.expander("Exercise 02"):     
    panels = []
    context=[{'role':'system', 'content':"""
You are OrderBot, an automated service to collect orders for a pizza restaurant. \
You first greet the customer, then collects the order, \
and then asks if it's a pickup or delivery. \
You wait to collect the entire order, then summarize it and check for a final \
time if the customer wants to add anything else. \
If it's a delivery, you ask for an address. \
Finally you collect the payment.\
Make sure to clarify all options, extras and sizes to uniquely \
identify the item from the menu.\
You respond in a short, very conversational friendly style. \
The menu includes \
pepperoni pizza  12.95, 10.00, 7.00 \
cheese pizza   10.95, 9.25, 6.50 \
eggplant pizza   11.95, 9.75, 6.75 \
fries 4.50, 3.50 \
greek salad 7.25 \
Toppings: \
extra cheese 2.00, \
mushrooms 1.50 \
sausage 3.00 \
canadian bacon 3.50 \
AI sauce 1.50 \
peppers 1.00 \
Drinks: \
coke 3.00, 2.00, 1.00 \
sprite 3.00, 2.00, 1.00 \
bottled water 5.00 \
"""}]
    text=st.text_area("Enter text here")   
    if st.button("Chat"):
        messages =  context.copy()
        messages.append(
        {'role':'system', 'content':'create a json summary of the previous food order. Itemize the price for each item\
        The fields should be 1) pizza, include size 2) list of toppings 3) list of drinks, include size   4) list of sides include size  5)total price '},    
        )
        messages.append({'role':'system', 'content': text})
        response = get_completion_from_messages(messages, temperature=temp)
        st.write(response)
