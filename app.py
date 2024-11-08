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
if 'codes' not in st.session_state:
    st.session_state.codes = []
if 'number_of_edits' not in st.session_state:
    st.session_state.number_of_edits = 0

#

#------------------- can be used to debug the code with specific buttons for the specific categories -------------------#
# # Initialize button states
# if 'button_states' not in st.session_state:
#     st.session_state.button_states = {
#         'reorder': False,
#         'highlighting': False,
#         'change_color': False,
#         'zooming': False,
#         'add_data': False,
#         'show_above_value': False,
#         'show_below_value': False,
#         'show_between_values': False,
#         'show_one_category': False,
#         'change_chart_type' : False,
#         'change_chart_type_better_fit': False
#     }
# # Function to handle button clicks
# def click_button(action):
#     for key in st.session_state.button_states.keys():
#         st.session_state.button_states[key] = (key == action)

# def open_buttons(code):
#     # Create buttons in columns
#     buttons = list()
#     buttons = list(st.session_state.button_states.keys())
#     columns = st.columns(len(buttons))

#     for idx, button in enumerate(buttons):
#         with columns[idx]:
#             if st.button(button):# , key=button):
#                 click_button(button)
  
#     # Perform actions based on button states
#     for action, state in st.session_state.button_states.items():
#         if state:
#             edit(code, action)



# reorder the bars to: NEAR BAY, INLAND, <1H OCEAN, ISLAND, NEAR OCEAN        
# make the bars green yellow orange red and purple
def user_edit_input():
    st.write("Enter your edit here")
    try:
        with st.form("my_form", clear_on_submit=True, border=False):
            input_value = st.text_input("Enter your edit here")
            submitted = st.form_submit_button("submit")
            if submitted:
                if input_value:
                    edit_type = test2.categorize(input_value) #here u get a chatcompletionmessage 
                    if edit_type.content == "other":
                        edit(edit_type.content, input_value)
                    else: 
                        edit_value = test2.extract_information(input_value)
                        edit(edit_type.content, edit_value.content)
    except Exception as e:
        st.session_state.number_of_edits += 1
        user_edit_input()
    return None


def edit(edit_type=None, input_value=None):
    st.session_state.number_of_edits += 1
    # Function to handle input and generate new code
    def handle_input(placeholder, code_generation_func, input_value):
        #user_input = st.text_input(placeholder, value=input_value or "", key=st.session_state.number_of_edits+20000)
        st.write(placeholder)
        st.write("input value: ",input_value)
        if input_value:
            #return [code_generation_func(old_code, user_input), user_input]
            return [code_generation_func(st.session_state.codes[-1], input_value), input_value]
        return None

    newcode = None

    # Process the new edit type and generate the new code
    if edit_type == None:
        st.subheader("no edit type")
        return
    if edit_type == "reorder":
        input = handle_input("reorder data (divide with a ',')", test2.reorder_data, input_value)
    elif edit_type == "highlight":
        input = handle_input("highlight (what do you want to highlight?)", test2.higlighting, input_value)
    elif edit_type == "change_color":
        input = handle_input("change color data (what color do you want?)", test2.change_color, input_value)
    elif edit_type == "zooming":
        input = handle_input("zooming (what width do you want?)", test2.zooming, input_value)
    elif edit_type == "add_data":
        input = handle_input("add data (what data do you want to add?)", test2.add_data, input_value)
    elif edit_type == "show_above_value":
        input = handle_input("show above value (above which value?)", test2.show_above_value, input_value)
    elif edit_type == "show_below_value":
        input = handle_input("show below value (below which value?)", test2.show_below_value, input_value)
    elif edit_type == "show_between_values":
        input = handle_input("show between values (between which values? divide with 'and')", test2.show_between_values, input_value)
    elif edit_type == "show_one_category":
        input = handle_input("show one category (which category?)", test2.show_one_category, input_value)
    elif edit_type == "change_chart_type":
        input = handle_input("change chart type", test2.change_chart_type, input_value)
    elif edit_type == "change_chart_type_better_fit":
        input = handle_input("change chart type better fit (which chart type?)", test2.change_chart_type_better_fit, input_value)
    elif edit_type == "other":
        input = handle_input("other (experimental)", test2.other, input_value)
    else:
        return

    if input is not None:
        newcode = input[0]
        input_value = input[1]

    if newcode is not None:
        # get the code from the chatgpt response
        newcode = test2.extract_code_v2(newcode)
        render_code(newcode, edit_type, input_value)

    
    
def render_code(newcode, edit_type, input_value):    
    if newcode == "No match found":
        edit(edit_type, input_value)
    else:
        try:
            exec_locals = {}
            exec(newcode, globals(), exec_locals)
            # Access the plot function from the local variables captured by exec()
            plot = exec_locals['plot']

            chart = plot(st.session_state.data)
            st.altair_chart(chart, use_container_width=True)
            st.session_state.codes.append(newcode)
            with st.expander("see new code"):
                st.code(newcode)
        except Exception as e:
            edit(edit_type, input_value)



def createDiagramm():
    
    library = "altair"
    textgen_config = TextGenerationConfig(n=1, temperature=0.2, model="gpt-4-turbo", use_cache=True)
    summary = st.session_state.summary
    charts = lida.visualize(summary, goal=st.session_state.goals[st.session_state.goalNumber], textgen_config=textgen_config, library=library)  

        
        #altair error fix 
        #this way would be way better for perfomance ut I didnt get it to run
        #charts[0].spec['data'] = {"url": path_to_save}
        #this way loads data directly and causes lots of memory usage > lag
    data_dict = st.session_state.data.to_dict(orient='records')
    charts[0].spec['data'] = {"values": data_dict}


        #display the chart    
    original = st.vega_lite_chart(charts[0].spec, use_container_width=True)
    if st.session_state.codes == []:
        st.session_state.codes.append(charts[0].code)
    with st.expander("see code"):
        st.code(charts[0].code)

    back = st.button("back", disabled=(len(st.session_state.codes) < 2))
    if back:
        st.session_state.codes.pop()
        st.session_state.number_of_edits = st.session_state.number_of_edits - 1
        render_code(st.session_state.codes[-1], None, None)

    user_edit_input()


        

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
    textgen_config = TextGenerationConfig(n=1, temperature=0.5, model="gpt-4o", use_cache=True)

    st.subheader("Summarization of your Data")
    file_uploader = st.file_uploader("Upload your CSV", type="csv")
    if file_uploader is not None:
        path_to_save = os.path.abspath("filename.csv")
        with open(path_to_save, "wb") as f:
            f.write(file_uploader.getvalue())

        data = pd.read_csv(path_to_save)
        st.write(data.head())

        summary = lida.summarize(path_to_save, summary_method="default", textgen_config=textgen_config)
        goals = lida.goals(summary, n=2, textgen_config=textgen_config)

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
            goalNumber=goalNumber+1
            
        ownGoal = st.text_input("Enter your own goal for Lida")
        if st.button("Submit"):
            if len(ownGoal) > 0:
                goals.append(ownGoal)
                st.session_state.goalNumber = len(goals) -1
                st.session_state.goals = goals
                st.session_state.page = "second"


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
        


            


