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
def higlighting(code, higlitght, summary):
    completion = client.chat.completions.create(
    model="gpt-4o",
      response_format={ "type": "text"},
      messages=[
        {"role": "system", "content": "You are a helpful assistant designed to change an altaire Code."},
        {"role": "user", "content": "Change this altaircode that it higlightes the "+ higlitght +" data and, when using altair code change bin to false and make sure the operator precedence is correct use parantheses when needed, begin the code with 'code:', end it with 'chart = plot(data)' for this altair code: "+code +" heres also a summary of the data for reference: "+ summary}
      ]
    )
    return completion.choices[0].message

#changing the color of the chart
def change_color(code, color, summary):
    completion = client.chat.completions.create(
      model="gpt-4o",
      response_format={ "type": "text"},
      messages=[
        {"role": "system", "content": "You are a helpful assistant designed to change an altaire Code."},
        {"role": "user", "content": "Change the color in this altaircode of the chart to "+color+" and begin the code with 'code:', end it with 'chart = plot(data)' for this altair code:"+code +" heres also a summary of the data for reference: "+summary}
      ]
    )
    return completion.choices[0].message

#zooming in the chart
def zooming(code, size, summary):
    completion = client.chat.completions.create(
      model="gpt-4o",
      response_format={ "type": "text"},
      messages=[
        {"role": "system", "content": "You are a helpful assistant designed to change an altaire Code."},
        {"role": "user", "content": "Zoom in on the chart, by zooming in to "+size+" and begin the code with 'code:', end it with 'chart = plot(data)' for this altair code:"+code +" heres also a summary of the data for reference: "+summary}
      ]
    )
    return completion.choices[0].message

#reordering data
def reorder_data(code, order, summary):
    completion = client.chat.completions.create(
      model="gpt-4o",
      response_format={ "type": "text"},
      messages=[
        {"role": "system", "content": "You are a helpful assistant designed to change an altaire Code."},
        {"role": "user", "content": "Reorder the data in the chart by setting the order of the categories to "+order+" and begin the code with 'code:', end it with 'chart = plot(data)' for this altair code:"+code +" heres also a summary of the data for reference: "+summary}
      ]
    )
    return completion.choices[0].message


#add data
def add_data(code, data, summary):
    completion = client.chat.completions.create(
      model="gpt-4o",
      response_format={ "type": "text"},
      messages=[
        {"role": "system", "content": "You are a helpful assistant designed to change an altaire Code."},
        {"role": "user", "content": "Add the data "+ data + " to the chart. Begin the code with 'code:', end it with 'chart = plot(data)' for this altair code:"+code +" heres also a summary of the data for reference: "+summary}
      ]
    )
    return completion.choices[0].message

#show only values above a certain value
def show_above_value(code, value, summary):
    completion = client.chat.completions.create(
      model="gpt-4o",
      response_format={ "type": "text"},
      messages=[
        {"role": "system", "content": "You are a helpful assistant designed to change an altaire Code."},
        {"role": "user", "content": "Show only values above a certain value in the chart by setting the value to "+value+" and begin the code with 'code:', end it with 'chart = plot(data)' for this altair code:"+code +" heres also a summary of the data for reference: "+summary}
      ]
    )
    return completion.choices[0].message

#show only values below a certain value
def show_below_value(code, value, summary):
    completion = client.chat.completions.create(
      model="gpt-4o",
      response_format={ "type": "text"},
      messages=[
        {"role": "system", "content": "You are a helpful assistant designed to change an altaire Code."},
        {"role": "user", "content": "Show only values below a certain value in the chart by setting the value to "+value+" and begin the code with 'code:', end it with 'chart = plot(data)' for this altair code:"+code +" heres also a summary of the data for reference: "+summary}
      ]
    )
    return completion.choices[0].message

#show only values between two values
def show_between_values(code, value, summary):
    completion = client.chat.completions.create(
      model="gpt-4o",
      response_format={ "type": "text"},
      messages=[
        {"role": "system", "content": "You are a helpful assistant designed to change an altaire Code."},
        {"role": "user", "content": "Show only values between two values in the chart by setting the values to "+value+", make sure the data is case-insensitive and begin the code with 'code:', end it with 'chart = plot(data)' for this altair code:"+code +" heres also a summary of the data for reference: "+summary}
      ]
    )
    return completion.choices[0].message

#show only one category
def show_one_category(code, category, summary):
    completion = client.chat.completions.create(
      model="gpt-4o",
      response_format={ "type": "text"},
      messages=[
        {"role": "system", "content": "You are a helpful assistant designed to change an altaire Code."},
        {"role": "user", "content": "Show only one category in the chart by setting the category to "+category+" and begin the code with 'code:', end it with 'chart = plot(data)' for this altair code:"+code +" heres also a summary of the data for reference: "+summary}
      ]
    )
    return completion.choices[0].message

#change chart type
def change_chart_type(code, chart_type, summary):
    completion = client.chat.completions.create(
      model="gpt-4o",
      response_format={ "type": "text"},
      messages=[
        {"role": "system", "content": "You are a helpful assistant designed to change an altaire Code."},
        {"role": "user", "content": "Change the chart type to "+chart_type+" and begin the code with 'code:', end it with 'chart = plot(data)' for this altair code:"+code +" heres also a summary of the data for reference: "+summary}
      ]
    )
    return completion.choices[0].message

#chage chart type to better fit the data given no chart type
def change_chart_type_better_fit(code, nothing, summary):
    completion = client.chat.completions.create(
      model="gpt-4o",
      response_format={ "type": "text"},
      messages=[
        {"role": "system", "content": "You are a helpful assistant designed to change an altaire Code."},
        {"role": "user", "content": "Change the chart type to better fit the data and begin the code with 'code:', end it with 'chart = plot(data)' for this altair code:"+code +" heres also a summary of the data for reference: "+summary}
      ]
    )
    return completion.choices[0].message

def other(code, message, summary):
    completion = client.chat.completions.create(
      model="gpt-4o",
      response_format={ "type": "text"},
      messages=[
        {"role": "system", "content": "You are a helpful assistant designed to change an altaire Code."},
        {"role": "user", "content": message + ". and begin the code with 'code:', end it with 'chart = plot(data)' for this altair code: " + code +" heres also a summary of the data for reference: "+summary}
      ]
    )
    return completion.choices[0].message

def translate(text):
    print("translated")
    textmessage = """Translate the given text to english. Here is the given text: """+text+". Just respond with the translated text. If the text is already in english, just respond with the same text."
    completion = client.chat.completions.create(
      model="gpt-4o",
      response_format={ "type": "text"},
      messages=[
        {"role": "system", "content": "You are a helpful assistant designed to translate the given text to english."},
        {"role": "user", "content": textmessage}
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
    patternCode = r"\)atad\(tolp = trahc(.*?)\:edoc"
    # Pattern to find the last occurrence of the reversed "```python" followed by the reversed "chart = plot(data)"
    patternPython = r"\)atad\(tolp = trahc(.*?)nohtyp```"
    # Find all matches
    match1 = re.search(patternCode, reversed_txt, re.DOTALL)
    match2 = re.search(patternPython, reversed_txt, re.DOTALL)
    # Determine the smallest match
    if match1 and match2:
        # Compare lengths of matched substrings
        if len(match1.group(1)) < len(match2.group(1)):
            smallest_match = match1.group(1)
        else:
            smallest_match = match2.group(1)
    elif match1:
        smallest_match = match1.group(1)
    elif match2:
        smallest_match = match2.group(1)
    else:
        return "No match found"
    # Reverse the smallest match to get the original order
    return smallest_match[::-1]

def translate(text):
    textmessage = """Translate the given text to english. Here is the given text: """+text+". Just respond with the translated text. If the text is already in english, just respond with the same text."
    completion = client.chat.completions.create(
      model="gpt-4o",
      response_format={ "type": "text"},
      messages=[
        {"role": "system", "content": "You are a helpful assistant designed to translate the given text to english."},
        {"role": "user", "content": textmessage}
      ]
    )
    return completion.choices[0].message
    
#categorice function given natural language to code
def categorize(text):
    textmessage = """Classify the given natural language into one of the following categories: change_color, highlight, zoom, reorder, add_data, show_above_value, show_below_value, show_between_values, show_one_category, change_chart_type, change_chart_type_better_fit and other. Here are some examples for the classification:         ["Change the color of the chart to green", "change_color"],
        ["Highlight the 'inland' data", "highlight"],
        ["Zoom in on the upper right corner of the boxplot", "zoom"],
        ["Reorder the data in the boxplot", "reorder"],
        ["Add data to the chart", "add_data"],
        ["Show only values above a certain value", "show_above_value"],
        ["Show only values below a certain value", "show_below_value"],
        ["Show only values between two values", "show_between_values"],
        ["Show only one category", "show_one_category"],
        ["Change the chart type to pie", "change_chart_type"],
        ["Change the chart type to better fit the data", "change_chart_type_better_fit"]
        ["change the size of the bars in the bar chart to stretch over 2 years instead of 5", "other"]
        Here is the given natural language: """+text+". Just respond with the category of the given natural language."
    
    completion = client.chat.completions.create(
      model="gpt-4o",
      response_format={ "type": "text"},
      messages=[
        {"role": "system", "content": "You are a helpful assistant designed to categorize the given natural language."},
        {"role": "user", "content": textmessage}
      ]
    )
    return completion.choices[0].message

def extract_category(chatcompletionmessage):
    category = chatcompletionmessage.content
    #match1 = re.search(patternCode, reversed_txt, re.DOTALL)
    category = re.search( r'content=(.*?)role=', category)
    return category
# streamlit run C://Users/levid/Desktop/Uni/Master/WiSe2324/Projekt1/Lida-project/app.py

def extract_information(text):  #subject to change
    textmessage = """extract the information needed to change the code from the given natural Language. the categories are change_color, highlight, zoom, reorder, add_data, show_above_value, show_below_value, show_between_values, show_one_category, change_chart_type, change_chart_type_better_fit and other. Here are some examples:
      ["I want a bar chart with bars that transition in color from red on the left to blue on the right.", "transition from red on the left to blue on the right"],
      a second example for change_color: ["Change the color of the chart to green", "green"],
      ["highlight the housing median ages of 20-30 by making them green", "housing median ages of 20-30 by making them green"],
      ["Zoom in on the upper right corner of the boxplot", "upper right corner"],
      ["Reorder the data in the boxplot in this order: NEAR BAY, INLAND, <1H OCEAN, ISLAND, NEAR OCEAN", "NEAR BAY, INLAND, <1H OCEAN, ISLAND, NEAR OCEAN"],
      ["Add this data point to the chart: Munich, 1.5 million inhabitnats, 25000sqm, 4000€ average housing spendings", "Munich, 1.5 million inhabitnats, 25000sqm, 4000€ average housing spendings"],
      ["Show only values above a housing cost of 3000", "3000"],
      ["Show only values below a housing cost of 3000", "3000"],
      ["Show only values between housing cost of 3000 and 4000", "3000 and 4000"],
      ["Show only Near Bay", "Near Bay"],
      ["Change the chart type to pie", "pie"],
      ["Change the chart type to better fit the data", "better fit the data"]
      Here is the given natural language: """+text+". Just respond with the information needed to change the code of the given natural language."
    
    completion = client.chat.completions.create(
      model="gpt-4o",
      response_format={ "type": "text"},
      messages=[
        {"role": "system", "content": "You are a helpful assistant designed to categorize the given natural language."},
        {"role": "user", "content": textmessage}
      ]
    )
    return completion.choices[0].message

def extract_information_from_message(chatcompletionmessage):
    information = chatcompletionmessage.content
    #match1 = re.search(patternCode, reversed_txt, re.DOTALL)
    information = re.search( r'content=(.*?)role=', information)
    return information


#print(extract_code(str(higlighting(code, higlitght))))
#print(extract_code(str(change_color(code, color))))
#print(extract_code(str(zooming(code, size))))
#print(extract_code(str(reorder_data(code, order))))
#print(extract_code(str(add_data(code, data))))
#print(extract_code(str(show_above_value(code, "10"))))
#print(extract_code(str(show_below_value(code, "10"))))
#print(extract_code(str(show_between_values(code, "5 and 10"))))
#print(extract_code(str(show_one_category(code, category))))
#print(extract_code(str(change_chart_type(code, "pie"))))
#print(extract_code(str(change_chart_type_better_fit(code))))
#print(categorize("Make the category Near_Bay stand out in the boxplot."))
#print(additional_information("Make the Bar NEAR_BAY stand out in the boxplot.", "highlight"))
# print(additional_information("Change the color of the chart to green", "change_color"))
# print(additional_information("Zoom in on the boxplot to the size of 200x100", "zooming"))
# #print(additional_information("Reorder the data in the boxplot", "reorder_data"))
# #print(additional_information("Add data to the chart", "add_data"))
# print(additional_information("Show only values above the value 30", "show_above_value"))
# print(categorize("Make the category Near_Bay stand out in the boxplot."))
#print(additional_information("Make the Bar NEAR_BAY stand out in the boxplot.", "highlight"))
#print(additional_information("Change the color of the chart to green", "change_color"))
#print(additional_information("Zoom in on the boxplot to the size of 200x100", "zooming"))
#print(additional_information("Reorder the data in the boxplot", "reorder_data"))
#print(additional_information("Add data to the chart", "add_data"))
#print(additional_information("Show only values above the value 30", "show_above_value"))

