import openai
import streamlit as st
from IPython.display import display, HTML
import json

def get_completion(prompt, model="gpt-3.5-turbo",temperature="0.7"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]

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




translation,universalTranslator,toneTransformation,formalConversion,spellCheck = st.tabs(["Translation","Universal Translator","Tone Transformation","Formal Conversion","Spell Check"])


with translation:
    st.header("Translation")

    text_area_values={
        "Prompt1": """Translate the following English text to Spanish: \ 
            ```Hi, I would like to order a blender```
            """,
        "Prompt2": """Tell me which language this is: 
            ```Combien coûte le lampadaire?```
            """,
        "Prompt3": """Translate the following  text to French and Spanish
            and English pirate: \
            ```I want to order a basketball```
            """,
        "Prompt4": """Translate the following text to Spanish in both the \
            formal and informal forms: 
            'Would you like to order a pillow?'
            """              
    }
    current_tab = st.selectbox("Select current tab", options=["Prompt1","Prompt2","Prompt3","Prompt4"])
    with st.form("translation"):
        text_area_values[current_tab] = st.text_area("Prompt to use or Modify", value=text_area_values[current_tab])
        submitted = st.form_submit_button("Submit")
    if submitted:
        prompt=text_area_values[current_tab]
        response = get_completion(prompt=prompt,temperature=temp)
        st.write(response)


with universalTranslator:
    st.header("Universal Translator")
    tokens=st.text_area("Enter a list of messages:","""La performance du système est plus lente que d'habitude.,
 Mi monitor tiene píxeles que no se iluminan.,
 Il mio mouse non funziona,
 Mój klawisz Ctrl jest zepsuty,
 我的屏幕在闪烁 """)
    sentences=tokens.split(",")
    with st.form("ut"):
        text_area_values[current_tab] = st.text_area("Prompt to use or Modify", value=text_area_values[current_tab])
        submitted = st.form_submit_button("Submit")
    if submitted:
        for sentence in sentences:
            prompt=f"Tell me what language this is: ```{sentence}```"
            lang = get_completion(prompt=prompt,temperature=temp)
            st.write(f"Original message ({lang}): {sentence}")
            prompt = f"""
    Translate the following  text to English \
    and Korean: ```{sentence}```
    """
            response=get_completion(prompt=prompt,temperature=temp)
            st.write(response)


with toneTransformation:
    st.header("Tone Transformation")
    prompt=st.text_area("Enter a message to change tone:","Translate the following from slang to a business letter: 'Dude, This is Joe, check out this spec on this standing lamp.")
    with st.form("tt"):
        st.write(prompt)
        submitted = st.form_submit_button("Submit")
    if submitted:
        response=get_completion(prompt=prompt,temperature=temp)
        st.write(response)    

with formalConversion:
    st.header("Formal Conversion")
    data_json = { "resturant employees" :[ 
    {"name":"Shyam", "email":"shyamjaiswal@gmail.com"},
    {"name":"Bob", "email":"bob32@gmail.com"},
    {"name":"Jai", "email":"jai87@gmail.com"}
    ]}
    prompt=st.text_area("Enter a message to change tone:","Translate the following python dictionary from JSON to an HTML table with column headers and title:")
    prompt=prompt+json.dumps(data_json)
    st.write(prompt)
    with st.form("fc"):
        st.write(prompt)
        submitted = st.form_submit_button("Submit")
    if submitted:
        response=get_completion(prompt=prompt,temperature=temp)
        st.write(response)
        st.write(HTML(response))     

with spellCheck:
    st.header("Spell Check and Grammer")    