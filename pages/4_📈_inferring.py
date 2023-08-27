import openai
import streamlit as st
from IPython.display import display, HTML

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


text_area_values = {
    "Sentiment01": """What is the sentiment of the following product review, 
which is delimited with triple backticks?

Review text:""",
    "Sentiment02": """What is the sentiment of the following product review, 
which is delimited with triple backticks?

Give your answer as a single word, either "positive" \
or "negative".

Review text:""",
    "Emotion": """Identify a list of emotions that the writer of the \
following review is expressing. Include no more than \
five items in the list. Format your answer as a list of \
lower-case words separated by commas.

Review text:""",
    "Anger": """Is the writer of the following review expressing anger?\
The review is delimited with triple backticks. \
Give your answer as either yes or no.

Review text: '""",
    "Extract product and company name from customer reviews": """Identify the following items from the review text: 
- Item purchased by reviewer
- Company that made the item

The review is delimited with triple backticks. \
Format your response as a JSON object with \
"Item" and "Brand" as the keys. 
If the information isn't present, use "unknown" \
as the value.
Make your response as short as possible.
  
Review text:""",
    "Multiple Tasks at once": """Identify the following items from the review text: 
- Sentiment (positive or negative)
- Is the reviewer expressing anger? (true or false)
- Item purchased by reviewer
- Company that made the item

The review is delimited with triple backticks. \
Format your response as a JSON object with \
"Sentiment", "Anger", "Item" and "Brand" as the keys.
If the information isn't present, use "unknown" \
as the value.
Make your response as short as possible.
Format the Anger value as a boolean.

Review text:""",
    "Inferring 5 Topics": """Determine five topics that are being discussed in the \
following text, which is delimited by triple backticks.

Make each item one or two words long. 

Format your response as a list of items separated by commas.

Text sample:""",
    "Alert on Topics": """Determine whether each item in the following list of \
topics is a topic in the text below, which
is delimited with triple backticks.

Give your answer as list with 0 or 1 for each topic.\

List of topics: {", ".join(topic_list)}

Text sample:""",
}

current_tab = st.selectbox("Select current tab", options=["Sentiment01", "Sentiment02", "Emotion","Anger","Extract product and company name from customer reviews","Multiple Tasks at once","Inferring 5 Topics","Alert on Topics"])
text_area_values[current_tab] = st.text_area("Enter text", value=text_area_values[current_tab])

# Access the selected tab's text_area value
instruction = text_area_values[current_tab]    
             


with st.form("my_form"):
    if current_tab=="Inferring 5 Topics" or current_tab=="Alert on Topics":
        story = """In a recent survey conducted by the government, 
                public sector employees were asked to rate their level 
                of satisfaction with the department they work at. 
                The results revealed that NASA was the most popular 
                department with a satisfaction rating of 95%.

                One NASA employee, John Smith, commented on the findings, 
                stating, "I'm not surprised that NASA came out on top. 
                It's a great place to work with amazing people and 
                incredible opportunities. I'm proud to be a part of 
                such an innovative organization.

                The results were also welcomed by NASA's management team, 
                with Director Tom Johnson stating, "We are thrilled to 
                hear that our employees are satisfied with their work at NASA. 
                We have a talented and dedicated team who work tirelessly 
                to achieve our goals, and it's fantastic to see that their 
                hard work is paying off.

                The survey also revealed that the 
                Social Security Administration had the lowest satisfaction 
                rating, with only 45% of employees indicating they were 
                satisfied with their job. The government has pledged to 
                address the concerns raised by employees in the survey and 
                work towards improving job satisfaction across all departments.
                """
    else:
        story="""Needed a nice lamp for my bedroom, and this one had \
            additional storage and not too high of a price point. \
            Got it fast.  The string to our lamp broke during the \
            transit and the company happily sent over a new one. \
            Came within a few days as well. It was easy to put \
            together.  I had a missing part, so I contacted their \
            support and they very quickly got me the missing piece! \
            Lumina seems to me to be a great company that cares \
            about their customers and products!!"""
    review = st.text_area("Product Review",story,height=100)
    
    html=st.checkbox("Looking for a HTML Response?")
    submitted = st.form_submit_button("Submit")

    
    if submitted:
        prompt=instruction+" \""+review+"\""
        response = get_completion(prompt=prompt,temperature=temp)
        if html := True:
            st.write(HTML(response))
        else:
            st.write(response)
        if current_tab=="Inferring 5 Topics" or current_tab=="Alert on Topics":
            response.split(sep=',')
            topic_list = [
                "nasa", "local government", "engineering", 
                "employee satisfaction", "federal government"
            ]
            prompt = f"""
            Determine whether each item in the following list of \
            topics is a topic in the text below, which
            is delimited with triple backticks.

            Give your answer as list with 0 or 1 for each topic.\

            List of topics: {", ".join(topic_list)}

            Text sample: {story}
            """
            #st.write(prompt)
            response = get_completion(prompt=prompt,temperature=temp)
            if html := True:
                st.write(HTML(response))
            else:
                st.write(response)

            # topic_dict = {i.split(': ')[0]: int(i.split(': ')[1]) for i in response.split(sep='\n')}
            # if topic_dict['nasa'] == 0:
            #     st.write("ALERT: New NASA story!")
        
       


