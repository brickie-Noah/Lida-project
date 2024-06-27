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
if 'goalNumber' not in st.session_state:
    st.session_state.goalNumber = 0
if 'data' not in st.session_state:
    st.session_state.data = None


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


############ THIS WAS USED PREVIOUSLY IF WE USE A METHOD LIKE IN THE COMMENTED CODE AT THE BOTTOM WE CAN USE THIS ##############
# #lida gives a base64 string which we convert to a image here
# def base64_to_image(base64_string):
#     byte_data = base64.b64decode(base64_string)
#     # Use BytesIO to convert the byte data to image
#     return Image.open(BytesIO(byte_data))


def edit(charts, data, type):
        newcode = None
        # Process the new edit type and generate the new code
        if type == "reorder":
            # NEAR BAY, INLAND, <1H OCEAN, ISLAND, NEAR OCEAN
            reorder = st.text_input("reorder data", placeholder="divide with a ','")
            if reorder:
                newcode = test2.reorder_data(charts[0].code, reorder)
        elif type == "highlighting":
            highlighting = st.text_input("highlight", placeholder="what do you want to highlight?")
            if highlighting:
                newcode = test2.higlighting(charts[0].code, highlighting)
        elif type == "change_color":
            change_color = st.text_input("change color data", placeholder="what color do you want?")
            if change_color:
                newcode = test2.change_color(charts[0].code, change_color)
        elif type == "zooming":
            zooming = st.text_input("zooming", placeholder="what width do you want?")
            if zooming:
                newcode = test2.zooming(charts[0].code, zooming)
        elif type == "add_data":
            add_data = st.text_input("add data", placeholder="what data do you want to add?")
            if add_data:
                newcode = test2.add_data(charts[0].code, add_data)
        elif type == "show_above_value":
            show_above_value = st.text_input("show above value", placeholder="above which value?")
            if show_above_value:
                newcode = test2.show_above_value(charts[0].code, show_above_value)
        elif type == "show_below_value":
            show_below_value = st.text_input("show below value", placeholder="below which value?")
            if show_below_value:
                newcode = test2.show_below_value(charts[0].code, show_below_value)
        elif type == "show_between_values":
            show_between_values = st.text_input("show between values", placeholder="between which values? (divide with a 'and')")
            if show_between_values:
                newcode = test2.show_between_values(charts[0].code, show_between_values)
        elif type == "show_one_category":
            show_one_category = st.text_input("show one category", placeholder="which category?")
            if show_one_category:
                newcode = test2.show_one_category(charts[0].code, show_one_category)
        elif type == "change_chart_type_better_fit":
            change_chart_type_better_fit = st.text_input("change chart type better fit", placeholder="which chart type?")
            if change_chart_type_better_fit:
                newcode = test2.change_chart_type_better_fit(charts[0].code, change_chart_type_better_fit)

        if newcode is not None:
            # get the code from the chatgpt response
            newcode = test2.extract_code_v2(newcode)

            exec_locals = {}
            exec(newcode, globals(), exec_locals)
            # Access the plot function from the local variables captured by exec()
            plot = exec_locals['plot']

            #st.write("reordered chart")
            chart = plot(data)
            st.altair_chart(chart, use_container_width=True)
            with st.expander("see new code"):
                st.code(newcode)


def createDiagramm():
    library = "altair"
    textgen_config = TextGenerationConfig(n=1, temperature=0.2, use_cache=True)
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
            st.write(f"Displaying diagram for {action}")
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

    #menu = st.sidebar.selectbox("Choose an Option", ["Summarize", "Question based Graph"])

    #if menu == "Summarize":
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
        

# THIS WAS A PAGE WHERE YOU COULD WRITE YOUR OWN GOAL TO LIDA 
# SOMETHING LIKE THAT WILL BE NEEDED FOR THE FINAL PRODUCT

#elif menu == "Question based Graph":
    # st.subheader("Query your Data to Generate Graph")
    # file_uploader = st.file_uploader("Upload your CSV", type="csv")
    # if file_uploader is not None:
    #     path_to_save = "filename1.csv"
    #     with open(path_to_save, "wb") as f:
    #         f.write(file_uploader.getvalue())
    #     text_area = st.text_area("Query your Data to Generate Graph", height=200)
    #     if st.button("Generate Graph"):
    #         if len(text_area) > 0:
    #             st.info("Your Query: " + text_area)
    #             lida = Manager(text_gen = llm("openai")) 
    #             textgen_config = TextGenerationConfig(n=1, temperature=0.2, use_cache=True)
    #             summary = lida.summarize("filename1.csv", summary_method="default", textgen_config=textgen_config)
    #             user_query = text_area
    #             library = "seaborn"
    #             charts = lida.visualize(summary=summary, goal=user_query, textgen_config=textgen_config, library=library)  
    #             charts[0]
    #             image_base64 = charts[0].raster
    #             img = base64_to_image(image_base64)
    #             st.image(img)
            


