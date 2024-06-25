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

#states so stuff can be used like toggle buttons
if 'reorder' not in st.session_state:
    st.session_state.reorder = False
def click_button_reorder():
    st.session_state.reorder = True

# # Initialize button states
# button_states = {
#     'reorder': False,
#     'highlighting': False,
#     'change_color': False,
#     'zooming': False,
#     'add_data': False,
#     'show_above_value': False,
#     'show_below_value': False,
#     'show_between_values': False,
#     'show_one_category': False,
# }
# # Function to handle button clicks
# def click_button(action):
#     for key in button_states.keys():
#         button_states[key] = (key == action)


############ THIS WAS USED PREVIOUSLY IF WE USE A METHOD LIKE IN THE COMMENTED CODE AT THE BOTTOM WE CAN USE THIS ##############
# #lida gives a base64 string which we convert to a image here
# def base64_to_image(base64_string):
#     byte_data = base64.b64decode(base64_string)
#     # Use BytesIO to convert the byte data to image
#     return Image.open(BytesIO(byte_data))


def reorder(charts, data, type):
    # NEAR BAY, INLAND, <1H OCEAN, ISLAND, NEAR OCEAN
    order = st.text_input("reorder data", placeholder="divide with a ','")#, key=i)
    if order:
        # Process the new order
        newcode = test2.reorder_data(charts[0].code, order)
        newcode = test2.extract_code_v2(newcode)



        exec_locals = {}
        exec(newcode, globals(), exec_locals)
        # Access the plot function from the local variables captured by exec()
        plot = exec_locals['plot']

        st.write("reordered chart")
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
    st.title("fixed Chart Executor Response Visualization")
    
    original = st.vega_lite_chart(charts[0].spec, use_container_width=True)
    with st.expander("see code"):
                st.code(charts[0].code)
    # if st.button("reorder data"):
    #     reorder(charts)


    st.button('reorder', on_click=click_button_reorder)
    # st.button('higlighting', on_click=click_button_reorder)
    # st.button('change_color', on_click=click_button_reorder)
    # st.button('zooming', on_click=click_button_reorder)
    # st.button('add_data', on_click=click_button_reorder)
    # st.button('show_above_value', on_click=click_button_reorder)
    # st.button('show_below_value', on_click=click_button_reorder)
    # st.button('show_between_values', on_click=click_button_reorder)
    # st.button('show_one_category', on_click=click_button_reorder)

    if st.session_state.reorder:
        reorder(charts, st.session_state.data, "reorder")
    # if st.session_state.higlighting:
    #     reorder(charts, st.session_state.data, "higlighting")


    # # Create buttons
    # buttons = button_states.keys()
    # for button in buttons:
    #     if st.button(button, key=button):
    #         click_button(button)
    
    # # Perform actions based on button states
    # for action, state in button_states.items():
    #     if state:
    #         reorder(charts, st.session_state.data, action)
        


    
        

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
        st.write(f"nach summary erstellung summary_dict {type(summary_dict)}")
        st.write(f"nach summary erstellung summary {type(summary)}")
    st.write(f"sessionstate.summary am ende {type(st.session_state.summary)}")
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
            


