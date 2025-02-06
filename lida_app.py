import streamlit as st 
from lida import Manager, TextGenerationConfig , llm  
from dotenv import load_dotenv
import os
import openai
import test2
import altair as alt
from lida.datamodel import Summary
import pandas as pd

lida = Manager(text_gen = llm("openai"))

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

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
# if 'number_of_edits' not in st.session_state:
#     st.session_state.number_of_edits = 0
if 'specs' not in st.session_state:
    st.session_state.specs = []

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

def createDiagramm():
    
    library = "altair"
    textgen_config = TextGenerationConfig(n=1, temperature=0.5, model="gpt-4-turbo", use_cache=True)
    summary = st.session_state.summary
    charts = lida.visualize(summary, goal=st.session_state.goals[st.session_state.goalNumber], textgen_config=textgen_config, library=library)  

        
        #altair error fix 
        #this way would be way better for perfomance ut I didnt get it to run
        #charts[0].spec['data'] = {"url": path_to_save}
        #this way loads data directly and causes lots of memory usage > lag
    data_dict = st.session_state.data.to_dict(orient='records')
    charts[0].spec['data'] = {"values": data_dict}
    #if len(st.session_state.codes) == 0:
    st.vega_lite_chart(charts[0].spec, use_container_width=True)
    if st.session_state.codes == []:
        st.session_state.codes.append(charts[0].code)
        st.write("code appended from createDiagramm")
    with st.expander("see code"):
        st.code(charts[0].code)
    # try:
    #     render_code(charts[0].code, st.session_state.data)
    #     if len(st.session_state.codes) == 0:
    #         st.session_state.codes.append(charts[0].code)
    # except Exception as e:
    #     createDiagramm()

    # back = st.button("back", disabled=(len(st.session_state.codes) <= 2))
    # if back:
    #     st.session_state.codes.pop()
    #     #st.session_state.number_of_edits = st.session_state.number_of_edits - 1
    #     render_code(st.session_state.codes[-1], None)

    user_edit_input()
    #user_edit_input()


def user_edit_input():
    if len(st.session_state.codes) >= 1:
        back = st.button("back", disabled=(len(st.session_state.codes) <= 2))
        if back:
            st.session_state.codes.pop()
            render_code(st.session_state.codes[-1], st.session_state.data, True)

    try:
        with st.form("my_form", clear_on_submit=True, border=False):
            input_value = st.text_input("Enter your edit here")
            submitted = st.form_submit_button("submit")
            if submitted:
                if input_value:

                    charts = lida.edit(code=st.session_state.codes[-1], summary=st.session_state.summary, instructions=input_value, library="altair", textgen_config=TextGenerationConfig(n=1, temperature=0.5, model="gpt-4o", use_cache=True))
                    data_dict = st.session_state.data.to_dict(orient='records')
                    charts[0].spec['data'] = {"values": data_dict}
                    render_code(charts[0].code, st.session_state.data, False)
    except Exception as e:
        #st.session_state.number_of_edits += 1
        user_edit_input()
    return None


def render_code(code, data, back_button=False):
    try:
        exec_locals = {'data': data}
        exec(code, globals(), exec_locals)
        # Access the plot function from the local variables captured by exec()
        plot = exec_locals['plot']

        chart = plot(data)
        st.altair_chart(chart, use_container_width=True)
        if back_button == False:
            st.session_state.codes.append(code)
        with st.expander("see code"):
            st.code(code)
    except Exception as e:
        st.write("Error in displaying the chart with code", str(e))
        #edit(edit_type, input_value)
    

def display_first_page():
    textgen_config = TextGenerationConfig(n=1, temperature=0.5, model="gpt-4o", use_cache=True)

    st.subheader("Summarization of your Data")
    file_uploader = st.file_uploader("Upload your CSV", type="csv")
    if file_uploader is not None:
        path_to_save = os.path.abspath("filename_Lida.csv")
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

#-----------------------------------------------------------------------------------------------------------------------------------------------

#     library = "altair"
#     textgen_config = TextGenerationConfig(n=1, temperature=0.2, model="gpt-4-turbo", use_cache=True)

    
#     charts = lida.visualize(summary, goal=goals[0], textgen_config=textgen_config, library=library)  

        

#     data_dict = data.to_dict(orient='records')
#     charts[0].spec['data'] = {"values": data_dict}
#     st.session_state.data = data
#     input_code = """
# import altair as alt
# import pandas as pd

# def plot(data: pd.DataFrame):
#     chart = alt.Chart(data).mark_boxplot().encode(
#         x=alt.X('ocean_proximity', title='Ocean Proximity'),
#         y=alt.Y('median_house_value', title='Median House Value'),
#         color='ocean_proximity'
#     ).properties(
#         title="Distribution of Median House Value by Ocean Proximity"
#     )
#     return chart

# chart = plot(data)
# """
#     render_code(input_code, data)
#-----------------------------------------------------------------------------------------------------------------------------------------------	

        # st.session_state.summary = summary
        # st.session_state.goals = goals
        # st.session_state.data = data

        # goalNumber=0
        # for goal in goals:
        #     st.write(goal.question)
        #     toggle = st.checkbox("choose this goal",value=False, key=goalNumber)
        #     with st.expander("see rational and visualization"):
        #         st.write(goal.rationale + "\n\n" + goal.visualization)
        #     if toggle:
        #         st.session_state.goalNumber = goalNumber
        #         st.session_state.page = "second"
        #     goalNumber=goalNumber+1
            
        # ownGoal = st.text_input("Enter your own goal for Lida")
        # if st.button("Submit"):
        #     if len(ownGoal) > 0:
        #         goals.append(ownGoal)
        #         st.session_state.goalNumber = len(goals) -1
        #         st.session_state.goals = goals
        #         st.session_state.page = "second"



pages = {
    "first": display_first_page,
    "second": display_second_page,
    #"third": display_third_page
} 
# Display the current page based on session state
pages[st.session_state.page]()