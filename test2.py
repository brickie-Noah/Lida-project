import os
from openai import OpenAI
from dotenv import load_dotenv
import re

load_dotenv()
OpenAI.api_key = os.getenv('OPENAI_API_KEY')

client = OpenAI()

code = "import altair as alt\nimport pandas as pd\n\ndef plot(data: pd.DataFrame):\n    data['median_income'] = pd.to_numeric(data['median_income'], errors='coerce')\n    data = data[pd.notna(data['median_income'])]\n    chart = alt.Chart(data).mark_boxplot().encode(\n        x=alt.X('ocean_proximity:N', axis=alt.Axis(title='Ocean Proximity')),\n        y=alt.Y('median_income:Q', axis=alt.Axis(title='Median Income')),\n        color=alt.Color('ocean_proximity:N', legend=alt.Legend(title='Ocean Proximity'), scale=alt.Scale(scheme='category10'))\n    ).properties(title='Distribution of Median Income Across Different Ocean Proximity Categories')\n    return chart\n\nchart = plot(data)"

higlitght = "inland"
color = "green"
size = "500x300"
order = "['NEAR BAY', 'INLAND', 'NEAR OCEAN', 'ISLAND', '<1H OCEAN']"
data = "{'ocean_proximity': ['NEAR BAY', 'INLAND', 'NEAR OCEAN', 'ISLAND', '<1H OCEAN'], 'median_income': [50000, 60000, 70000, 80000, 90000]}"
category = "INLAND"

#highghlithing in the given code
def higlighting(code, higlitght):
    completion = client.chat.completions.create(
    model="gpt-4-turbo",
      response_format={ "type": "text"},
      messages=[
        {"role": "system", "content": "You are a helpful assistant designed to change an altaire Code."},
        {"role": "user", "content": "Change this altaircode that it higlightes the "+ higlitght +" data and begin the code with 'code:' for this altair code:"+code}
      ]
    )
    return completion.choices[0].message

#changing the color of the chart
def change_color(code, color):
    completion = client.chat.completions.create(
      model="gpt-4-turbo",
      response_format={ "type": "text"},
      messages=[
        {"role": "system", "content": "You are a helpful assistant designed to change an altaire Code."},
        {"role": "user", "content": "Change the color in this altaircode of the chart to "+color+" and begin the code with 'code:' for this altair code:"+code}
      ]
    )
    return completion.choices[0].message

#zooming in the chart
def zooming(code, size):
    completion = client.chat.completions.create(
      model="gpt-4-turbo",
      response_format={ "type": "text"},
      messages=[
        {"role": "system", "content": "You are a helpful assistant designed to change an altaire Code."},
        {"role": "user", "content": "Zoom in on the boxplot by setting the width to"+size+" and begin the code with 'code:' for this altair code:"+code}
      ]
    )
    return completion.choices[0].message

#reordering data
def reorder_data(code, order):
    completion = client.chat.completions.create(
      model="gpt-4-turbo",
      response_format={ "type": "text"},
      messages=[
        {"role": "system", "content": "You are a helpful assistant designed to change an altaire Code."},
        {"role": "user", "content": "Reorder the data in the boxplot by setting the order of the categories to "+order+" and begin the code with 'code:' for this altair code:"+code}
      ]
    )
    return completion.choices[0].message


#add data
def add_data(code, data):
    completion = client.chat.completions.create(
      model="gpt-4-turbo",
      response_format={ "type": "text"},
      messages=[
        {"role": "system", "content": "You are a helpful assistant designed to change an altaire Code."},
        {"role": "user", "content": "Add the data "+ data + " to the chart. Begin the code with 'code:' for this altair code:"+code}
      ]
    )
    return completion.choices[0].message

#show only values above a certain value
def show_above_value(code, value):
    completion = client.chat.completions.create(
      model="gpt-4-turbo",
      response_format={ "type": "text"},
      messages=[
        {"role": "system", "content": "You are a helpful assistant designed to change an altaire Code."},
        {"role": "user", "content": "Show only values above a certain value in the boxplot by setting the value to "+value+" and begin the code with 'code:' for this altair code:"+code}
      ]
    )
    return completion.choices[0].message

#show only values below a certain value
def show_below_value(code, value):
    completion = client.chat.completions.create(
      model="gpt-4-turbo",
      response_format={ "type": "text"},
      messages=[
        {"role": "system", "content": "You are a helpful assistant designed to change an altaire Code."},
        {"role": "user", "content": "Show only values below a certain value in the boxplot by setting the value to "+value+" and begin the code with 'code:' for this altair code:"+code}
      ]
    )
    return completion.choices[0].message

#show only values between two values
def show_between_values(code, value):
    completion = client.chat.completions.create(
      model="gpt-4-turbo",
      response_format={ "type": "text"},
      messages=[
        {"role": "system", "content": "You are a helpful assistant designed to change an altaire Code."},
        {"role": "user", "content": "Show only values between two values in the boxplot by setting the values to "+value+" and begin the code with 'code:' for this altair code:"+code}
      ]
    )
    return completion.choices[0].message

#show only one category
def show_one_category(code, category):
    completion = client.chat.completions.create(
      model="gpt-4-turbo",
      response_format={ "type": "text"},
      messages=[
        {"role": "system", "content": "You are a helpful assistant designed to change an altaire Code."},
        {"role": "user", "content": "Show only one category in the boxplot by setting the category to "+category+" and begin the code with 'code:' for this altair code:"+code}
      ]
    )
    return completion.choices[0].message



def extract_code(text):
    code_blocks = re.findall(r'```(.*?)```', text, re.DOTALL)
    code_blocks = str(code_blocks).replace('\\n', "\n")
    code_blocks = code_blocks.replace("\\", "")
    #code_blocks = code_blocks.replace("'", "\\'")
    return code_blocks

def extract_code_v2(chatcompletionmessage):
    txt = chatcompletionmessage.content
    # Reverse the text
    reversed_txt = txt[::-1]
    # Pattern to find the last occurrence of the reversed "code:" followed by the reversed "chart = plot(data)"
    pattern = r"\)atad\(tolp = trahc(.*?)\:edoc"
    # Find all matches
    matches = re.findall(pattern, reversed_txt, re.DOTALL)
    # Reverse the matches to get the original order and take the first one as it corresponds to the last match in the original text
    x = [match[::-1] for match in matches]
    # Print the last match
    if x:
      return(x[0])
    else:
      return("No match found")


#print(extract_code(str(higlighting(code, higlitght))))
#print(extract_code(str(change_color(code, color))))
#print(extract_code(str(zooming(code, size))))
#print(extract_code(str(reorder_data(code, order))))
#print(extract_code(str(add_data(code, data))))
print(extract_code(str(show_above_value(code, "10"))))
print(extract_code(str(show_below_value(code, "10"))))
print(extract_code(str(show_between_values(code, "5 and 10"))))
#print(extract_code(str(show_one_category(code, category))))


