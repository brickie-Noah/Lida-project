import streamlit as st 
from lida import Manager, TextGenerationConfig , llm  
from dotenv import load_dotenv
import os
import openai
from openai import OpenAI
from PIL import Image
from io import BytesIO
import base64
import re
import pandas as pd
from IPython.display import display
import json
import gpt_client
import altair as alt
from lida.datamodel import Summary
import streamlit.components.v1 as components
import tempfile
from audiorecorder import audiorecorder


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
if 'backButton' not in st.session_state:
    st.session_state.backButton = False
if "edit_input_counter" not in st.session_state:
    st.session_state.edit_input_counter = 0

    # some examples for the user to see what he can do with the code:
        # reorder the bars to: NEAR BAY, INLAND, <1H OCEAN, ISLAND, NEAR OCEAN        
        # make the bars green yellow orange red and purple

# creates and handles the back button, creates forms for user input and extracts the categorie and the information of the user input
def user_edit_input():
    back = st.button("back")
    if back:
        if len(st.session_state.codes) >= 1:
            st.session_state.codes.pop()
            render_code(st.session_state.codes[-1], None, None, True)
        else:
            st.write("no code found")

    st.write("Enter your edit here")
    try:
        user_input_voice = None	
        col1, col2 = st.columns([5, 1])
        with col2:
            # voice recording and Whisper-Integration
            #outside of the form to allow for audio recording without submitting the form
            st.markdown("####")
            audio2 = audiorecorder("record 2", "stop 2", key="audio_recorder2")
            if len(audio2) > 0:
                audio2.export("recording2.wav", format="wav")
                with open("recording2.wav", "rb") as audio_file:
                    transcript = openai.audio.transcriptions.create(model="whisper-1", file=audio_file)
                user_input_voice = transcript.text
                transcript = None
                audio2 = None
                os.remove("recording2.wav")
            else:
                # If no audio, keep previous or empty
                st.session_state.edit_input = st.session_state.get("edit_input", "")

         # Form for user to enter text input and submit the edit
        with st.form("my_form", clear_on_submit=True, border=False):
            with col1:
                user_input_text = st.text_input("Enter your edit here", key="edit_input")
                
            # Use transcribed voice input if available, else text input
            if user_input_voice:
                st.write("Transcription: ", user_input_voice)
                user_input = user_input_voice
                user_input_voice = None
            else:
                user_input = user_input_text

            submitted = st.form_submit_button("submit")
            if submitted:
                if user_input:
                    make_edit(user_input)
    except Exception as e:
       st.error(f"Fehler: {e}")
    return None

def make_edit(user_input):
    try:
        input_translated = gpt_client.translate(user_input)
        edit_type = gpt_client.categorize(input_translated.content) #here u get a chatcompletionmessage 
        if edit_type.content == "other":
            edit(edit_type.content, input_translated.content)
        else: 
            edit_value = gpt_client.extract_information(input_translated.content)
            edit(edit_type.content, edit_value.content)
    except Exception as e:
        make_edit(user_input)  # Retry if an error occurs


# takes the inputed data and decides which GPT client function to use based on edit type, also extracts the graph code from the chatgpt response
def edit(edit_type=None, input_value=None):
    # Function to handle input and generate new code
    def handle_input(placeholder, code_generation_func, input_value):
        if input_value != None:
            summary_str = str(st.session_state.summary)
            return [code_generation_func(st.session_state.codes[-1], input_value, summary_str), input_value]
        return None

    newcode = None
    # Process the new edit type and generate the new code
    if edit_type == None:
        st.subheader("no edit type")
        return
    if edit_type == "reorder":
        gpt_code_answer = handle_input("reorder data (divide with a ',')", gpt_client.reorder_data, input_value)
    elif edit_type == "highlight":
        # e.g., Highlight specific chart elements
        gpt_code_answer = handle_input("highlight (what do you want to highlight?)", gpt_client.higlighting, input_value)
    elif edit_type == "change_color":
        gpt_code_answer = handle_input("change color data (what color do you want?)", gpt_client.change_color, input_value)
    elif edit_type == "zoom":
        gpt_code_answer = handle_input("zooming", gpt_client.zooming, input_value)
    elif edit_type == "add_data":
        gpt_code_answer = handle_input("add data (what data do you want to add?)", gpt_client.add_data, input_value)
    elif edit_type == "show_above_value":
        gpt_code_answer = handle_input("show above value (above which value?)", gpt_client.show_above_value, input_value)
    elif edit_type == "show_below_value":
        gpt_code_answer = handle_input("show below value (below which value?)", gpt_client.show_below_value, input_value)
    elif edit_type == "show_between_values":
        gpt_code_answer = handle_input("show between values (between which values? divide with 'and')", gpt_client.show_between_values, input_value)
    elif edit_type == "show_one_category":
        gpt_code_answer = handle_input("show one category (which category?)", gpt_client.show_one_category, input_value)
    elif edit_type == "change_chart_type":
        gpt_code_answer = handle_input("change chart type", gpt_client.change_chart_type, input_value)
    elif edit_type == "change_chart_type_better_fit":
        gpt_code_answer = handle_input("change chart type better fit (which chart type?)", gpt_client.change_chart_type_better_fit, input_value)
    elif edit_type == "other":
        gpt_code_answer = handle_input("other (experimental)", gpt_client.other, input_value)
    else:
        return
    


    if gpt_code_answer is not None:
        newcode = gpt_code_answer[0]

    if newcode is not None:
        # get the code from the chatgpt response
        newcode = gpt_client.extract_code_v2(newcode)
        render_code(newcode, edit_type, input_value)

    
# renders the chart from the code, if the code is not working edit is called which asks gpt tp make a new code
def render_code(newcode, edit_type, input_value, back_button=False):    
    if newcode == "No match found":
        edit(edit_type, input_value)
    else:
        try:
                exec_locals = {}
                # Execute the generated code to extract and display the Altair chart
                exec(newcode, globals(), exec_locals)
                # Access the plot function from the local variables captured by exec()
                plot = exec_locals['plot']

                chart = plot(st.session_state.data)
                st.altair_chart(chart, use_container_width=True)
                if not back_button:
                    st.session_state.codes.append(newcode)
                with st.expander("see new code"):
                    st.code(newcode)
        except Exception as e:
            # If generated code fails, re-run GPT to regenerate based on same edit
            edit(edit_type, input_value)


#creates the first diagramm from lida and also handles the back button
def createDiagramm():
    library = "altair"
    textgen_config = TextGenerationConfig(n=1, temperature=0.2, model="gpt-4-turbo", use_cache=True)
    summary = st.session_state.summary
    print(summary)
    charts = lida.visualize(summary, goal=st.session_state.goals[st.session_state.goalNumber], textgen_config=textgen_config, library=library)  

    data_dict = st.session_state.data.to_dict(orient='records')
    charts[0].spec['data'] = {"values": data_dict}

    #display the chart    
    original = st.vega_lite_chart(charts[0].spec, use_container_width=True)
    if st.session_state.codes == []:
        st.session_state.codes.append(charts[0].code)
    with st.expander("see code"):
        st.code(charts[0].code)
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

# Upload CSV and generate data summary + initial visualization goals using LIDA
# Let user pick a suggested goal or enter their own goal via text or voice
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

        goalNumber = 0
        for goal in goals:
            st.write(goal.question)
            toggle = st.checkbox("choose this goal", value=False, key=goalNumber)
            with st.expander("see rational and visualization"):
                st.write(goal.rationale + "\n\n" + goal.visualization)
            if toggle:
                st.session_state.goalNumber = goalNumber
                st.session_state.page = "second"
            goalNumber += 1

        # Input for own goal
        col1, col2 = st.columns([5, 1])
        with col1:
            user_input = st.text_input("Enter your own goal for Lida", key="goal_input")
        with col2:
            # Voice recording and Whisper integration
            st.markdown("####")
            audio = audiorecorder("record 1", "stop 1", key="audio_recorder1")
            if len(audio) > 0:
                audio.export("recording.wav", format="wav")
                with open("recording.wav", "rb") as audio_file:
                    transcript = openai.audio.transcriptions.create(model="whisper-1", file=audio_file)
                user_input = transcript.text
                os.remove("recording.wav")
        st.write("Transcription: ", user_input)


        if st.button("Submit"):
            ownGoal = user_input
            if len(ownGoal) > 0:
                goals.append(ownGoal)
                st.session_state.goalNumber = len(goals) - 1
                st.session_state.goals = goals
                st.session_state.page = "second"


################################### MANAGE THE DIFFERENT PAGES ##################################
# Dictionary to map page names to functions
pages = {
    "first": display_first_page,
    "second": display_second_page,
} 
# Initialize session state if not already done
if 'page' not in st.session_state:
    st.session_state.page = "first"
# Display the current page based on session state
pages[st.session_state.page]()
##################################################################################################
        


            


