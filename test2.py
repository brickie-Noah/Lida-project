from openai import OpenAI
import re
client = OpenAI()

code = "import altair as alt\nimport pandas as pd\n\ndef plot(data: pd.DataFrame):\n    data['median_income'] = pd.to_numeric(data['median_income'], errors='coerce')\n    data = data[pd.notna(data['median_income'])]\n    chart = alt.Chart(data).mark_boxplot().encode(\n        x=alt.X('ocean_proximity:N', axis=alt.Axis(title='Ocean Proximity')),\n        y=alt.Y('median_income:Q', axis=alt.Axis(title='Median Income')),\n        color=alt.Color('ocean_proximity:N', legend=alt.Legend(title='Ocean Proximity'), scale=alt.Scale(scheme='category10'))\n    ).properties(title='Distribution of Median Income Across Different Ocean Proximity Categories')\n    return chart\n\nchart = plot(data)"

higlitght = "inland"
color = "green"
size = "500x300"
order = "['NEAR BAY', 'INLAND', 'NEAR OCEAN', 'ISLAND', 'NEAR BAY']"
data = "data['median_income'] = pd.to_numeric(data['median_income'], errors='coerce')\n    data = data[pd.notna(data['median_income'])]"#?? daten ändern

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



def extract_code(text):
    code_blocks = re.findall(r'python\n(.*?)```', text, re.DOTALL)
    return code_blocks




print(higlighting(code))
#print(change_color(code))
#print(zooming(code))


