import lida

import streamlit as st 
from lida import Manager, TextGenerationConfig , llm  
from dotenv import load_dotenv
import os
import openai
from PIL import Image
from io import BytesIO
import base64
import re
import pandas as pd
from IPython.display import display
import json
import test2
import altair as alt
from lida.datamodel import Summary



lida = Manager(text_gen = llm("openai"))

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')


# Initialize session state variables
if 'page' not in st.session_state:
    st.session_state.page = "first"
if 'clic' not in st.session_state:
    st.session_state.clic = False
if 'summary' not in st.session_state:
    st.session_state.summary = None
if 'goals' not in st.session_state:
    st.session_state.goals = []
if 'ownGoal' not in st.session_state:
    st.session_state.ownGoal = None
if 'goalNumber' not in st.session_state:
    st.session_state.goalNumber = 0
if 'data' not in st.session_state:
    st.session_state.data = None
if 'input_value' not in st.session_state:
     st.session_state.input_value = None


# Initialize button states
if 'button_states' not in st.session_state:
    st.session_state.button_states = {
        'reorder': False,
        'highlighting': False,
        'change_color': False,
        'zooming': False,
        'add_data': False,
        'show_above_value': False,
        'show_below_value': False,
        'show_between_values': False,
        'show_one_category': False,
        'change_chart_type_better_fit': False
    }
# Function to handle button clicks
def click_button(action):
    for key in st.session_state.button_states.keys():
        st.session_state.button_states[key] = (key == action)






def edit(charts, data, type, input_value=None):
    # Function to handle input and generate new code
    def handle_input(placeholder, code_generation_func, input_value):
        if input_value is None:
            input_value = st.text_input(placeholder)
        if input_value:
            return [code_generation_func(charts[0].code, input_value), input_value]
        return None

    newcode = None
        # Process the new edit type and generate the new code
        #also 
        # NEAR BAY, INLAND, <1H OCEAN, ISLAND, NEAR OCEAN

    # Process the new edit type and generate the new code
    if type == "reorder":
        input = handle_input("reorder data (divide with a ',')", test2.reorder_data, input_value)
    elif type == "highlighting":
        input = handle_input("highlight (what do you want to highlight?)", test2.higlighting, input_value)
    elif type == "change_color":
        input = handle_input("change color data (what color do you want?)", test2.change_color, input_value)
    elif type == "zooming":
        input = handle_input("zooming (what width do you want?)", test2.zooming, input_value)
    elif type == "add_data":
        input = handle_input("add data (what data do you want to add?)", test2.add_data, input_value)
    elif type == "show_above_value":
        input = handle_input("show above value (above which value?)", test2.show_above_value, input_value)
    elif type == "show_below_value":
        input = handle_input("show below value (below which value?)", test2.show_below_value, input_value)
    elif type == "show_between_values":
        input = handle_input("show between values (between which values? divide with 'and')", test2.show_between_values, input_value)
    elif type == "show_one_category":
        input = handle_input("show one category (which category?)", test2.show_one_category, input_value)
    elif type == "change_chart_type_better_fit":
        input = handle_input("change chart type better fit (which chart type?)", test2.change_chart_type_better_fit, input_value)

    if input is not None:
        newcode = input[0]
        input_value = input[1]

    if newcode is not None:
        # get the code from the chatgpt response
        newcode = test2.extract_code_v2(newcode)

        if newcode == "No match found":
            edit(charts, data, type, input_value)
        else:
            try:
                exec_locals = {}
                exec(newcode, globals(), exec_locals)
                # Access the plot function from the local variables captured by exec()
                plot = exec_locals['plot']

                #st.write("reordered chart")
                chart = plot(data)
                st.altair_chart(chart, use_container_width=True)
                with st.expander("see new code"):
                    st.code(newcode)
            except Exception as e:
                edit(charts, data, type, input_value)


def createDiagramm():
    library = "altair"
    textgen_config = TextGenerationConfig(n=1, temperature=0.2, use_cache=True)
    summary = st.session_state.summary
    if st.session_state.goalNumber == 1000:
        #charts = lida.visualize(summary, goal=custom_goal, textgen_config=textgen_config, library=library)  
        #tempGoal = "what is the correleation between total rooms and population?"
        #ownGoal = st.session_state.ownGoal
        st.write("debug here")
        st.write("summary:",summary)
        st.write("textgen_config:",textgen_config)
        st.write("library:",library)
        charts = lida.visualize(summary, goal="what is the correleation between total rooms and population?", textgen_config=textgen_config, library=library)  
        #st.write(custom_goal.type)
        st.write(charts)
    else:
        st.write("debug here")
        st.write("summary:",summary)
        st.write("textgen_config:",textgen_config)
        st.write("library:",library)
        #charts = lida.visualize(summary, goal=st.session_state.goals[st.session_state.goalNumber], textgen_config=textgen_config, library=library)  
        charts = lida.visualize(summary, goal="what is the correleation between total rooms and population?", textgen_config=textgen_config, library=library)  
    
    #altair error fix 
    #this way would be way better for perfomance ut I didnt get it to run
    #charts[0].spec['data'] = {"url": path_to_save}
    #this way loads data directly and causes lots of memory usage > lag
    data_dict = st.session_state.data.to_dict(orient='records')
    charts[0].spec['data'] = {"values": data_dict}


    #display the chart    
    original = st.vega_lite_chart(charts[0].spec, use_container_width=True)
    with st.expander("see code"):
                st.code(charts[0].code)

    # Create buttons in columns
    buttons = list(st.session_state.button_states.keys())
    columns = st.columns(len(buttons))

    for idx, button in enumerate(buttons):
        with columns[idx]:
            if st.button(button, key=button):
                click_button(button)
  
    
    # Perform actions based on button states
    for action, state in st.session_state.button_states.items():
        if state:
            #st.write(f"Displaying diagram for {action}")
            edit(charts, st.session_state.data, action)
        

def display_second_page():
    st.subheader("Diagrams")
    # Convert summary dictionary to Summary object
    if isinstance(st.session_state.summary, dict):
        summary_dict = st.session_state.summary
        summary = Summary(
            name=summary_dict['name'],
            file_name=summary_dict['file_name'],
            dataset_description=summary_dict['dataset_description'],
            field_names=summary_dict['field_names'],
            fields=summary_dict['fields']
        )
        st.session_state.summary = summary  # Update the session state with the Summary object
    if 'data' in st.session_state and 'goalNumber' in st.session_state and 'summary' in st.session_state and 'goals' in st.session_state:
        createDiagramm()
    else:
        st.write("no data found")


def display_first_page():
    textgen_config = TextGenerationConfig(n=1, temperature=0.5, model="gpt-4-turbo", use_cache=True)

    menu = st.sidebar.selectbox("Choose an Option", ["Summarize", "Question based Graph"])

    if menu == "Summarize":
        st.subheader("Summarization of your Data")
        file_uploader = st.file_uploader("Upload your CSV", type="csv")
        if file_uploader is not None:
            #path_to_save = "filename.csv"
            path_to_save = os.path.abspath("filename.csv")
            with open(path_to_save, "wb") as f:
                f.write(file_uploader.getvalue())

            data = pd.read_csv(path_to_save)
            st.write(data.head())

            summary = lida.summarize(path_to_save, summary_method="default", textgen_config=textgen_config)
            goals = lida.goals(summary, n=2, textgen_config=textgen_config)

            #this doesnt exist "st.write(summary.file_name)" why is it working then?
            st.session_state.summary = summary
            st.session_state.goals = goals
            st.session_state.data = data

            goalNumber=0
            for goal in goals:
                st.write(goal.question)
                toggle = st.checkbox("choose this goal",value=False, key=goalNumber)
                with st.expander("see rational and visualization"):
                    st.write(goal.rationale + "\n\n" + goal.visualization)
                if toggle:
                    st.session_state.goalNumber = goalNumber
                    st.session_state.page = "second"
                    #createDiagramm(i, summary, goals, data)
                goalNumber=goalNumber+1
            
            #goals.append("Write your own goal")
            #####               what is the correleation between total rooms and population?
            ownGoal = st.text_input("Enter your own goal for Lida")
            if st.button("Submit"):
                if len(ownGoal) > 0:
                    st.session_state.goalNumber = 1000
                    st.session_state.ownGoal = ownGoal
                    st.session_state.page = "second"

                    # st.write(ownGoal)
                    # library = "altair"
                    # st.write("debug here")
                    # st.write("summary:",summary)
                    # st.write("textgen_config:",textgen_config)
                    # st.write("library:",library)
                    # #charts = lida.visualize(summary, goal="what is the correleation between total rooms and population?", textgen_config=textgen_config, library=library)  
                    # charts = lida.visualize(summary, goal=st.session_state.goals[0], textgen_config=textgen_config, library=library)  
                    # st.write(charts)

                #createDiagramm(len(goals), summary, goals, data)
        
############### THIS WAS A PAGE WHERE YOU COULD WRITE YOUR OWN GOAL TO LIDA ####################
# SOMETHING LIKE THAT WILL BE NEEDED FOR THE FINAL PRODUCT

    elif menu == "Question based Graph":
        st.subheader("Query your Data to Generate Graph")
        file_uploader = st.file_uploader("Upload your CSV", type="csv")
        if file_uploader is not None:
            path_to_save = "filename1.csv"
            with open(path_to_save, "wb") as f:
                f.write(file_uploader.getvalue())
            text_area = st.text_area("Query your Data to Generate Graph", height=200)
            if st.button("Generate Graph"):
                if len(text_area) > 0:
                    st.info("Your Query: " + text_area)
                    lida = Manager(text_gen = llm("openai")) 
                    textgen_config = TextGenerationConfig(n=1, temperature=0.2, use_cache=True)
                    summary = lida.summarize("filename1.csv", summary_method="default", textgen_config=textgen_config)
                    user_query = text_area
                    library = "altair"
                    charts = lida.visualize(summary=summary, goal="what is the correleation between total rooms and population?", textgen_config=textgen_config, library=library)  
                    charts[0]
                    image_base64 = charts[0].raster
                    img = base64_to_image(image_base64)
                    st.image(img)


############ THIS WAS USED PREVIOUSLY IF WE USE A METHOD LIKE IN THE COMMENTED CODE AT THE BOTTOM WE CAN USE THIS ##############
# #lida gives a base64 string which we convert to a image here
def base64_to_image(base64_string):
    byte_data = base64.b64decode(base64_string)
    # Use BytesIO to convert the byte data to image
    return Image.open(BytesIO(byte_data))

################################### MANAGE THE DIFFERENT PAGES ##################################
# Dictionary to map page names to functions
pages = {
    "first": display_first_page,
    "second": display_second_page,
    #"third": display_third_page
} 
# Initialize session state if not already done
if 'page' not in st.session_state:
    st.session_state.page = "first"
# Display the current page based on session state
pages[st.session_state.page]()
##################################################################################################
        


            


