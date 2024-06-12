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


load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

#lida gives a base64 string which we convert to a image here
def base64_to_image(base64_string):
    # Decode the base64 string
    byte_data = base64.b64decode(base64_string)
    
    # Use BytesIO to convert the byte data to image
    return Image.open(BytesIO(byte_data))

def createDiagramm(i):
    library = "altair"
    textgen_config = TextGenerationConfig(n=1, temperature=0.2, use_cache=True)
    charts = lida.visualize(summary=summary, goal=goals[i], textgen_config=textgen_config, library=library)  

    #altair error fix 
    #this way would be way better for perfomance ut I didnt get it to run
    #charts[0].spec['data'] = {"url": path_to_save}
    #this way loads data directly and causes lots of memory usage > lag
    data_dict = data.to_dict(orient='records')
    charts[0].spec['data'] = {"values": data_dict}

    #display the chart
    st.title("fixed Chart Executor Response Visualization")
    order = st.text_input("reorder data", placeholder="divide with a ','", key=i)
    original = st.vega_lite_chart(charts[0].spec, use_container_width=True)
    with st.expander("see code"):
                st.code(charts[0].code)
    # NEAR BAY, INLAND, <1H OCEAN, ISLAND, NEAR OCEAN
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
        





lida = Manager(text_gen = llm("openai"))
textgen_config = TextGenerationConfig(n=1, temperature=0.5, model="gpt-4-turbo", use_cache=True)

menu = st.sidebar.selectbox("Choose an Option", ["Summarize", "Question based Graph"])

if menu == "Summarize":
    st.subheader("Summarization of your Data")
    file_uploader = st.file_uploader("Upload your CSV", type="csv")
    if file_uploader is not None:
        path_to_save = "filename.csv"
        with open(path_to_save, "wb") as f:
            f.write(file_uploader.getvalue())

        data = pd.read_csv(path_to_save)
        st.write(data.head())

        summary = lida.summarize("filename.csv", summary_method="default", textgen_config=textgen_config)
        goals = lida.goals(summary, n=2, textgen_config=textgen_config)
        i=0
        for goal in goals:
            #col1, col2 = st.columns([0.75,0.25])
            #with col1:
            st.write(goal.question)
            #with col2:
            if st.toggle("choose this goal", i, disabled=False):
                createDiagramm(i)
            with st.expander("see rational and visualization"):
                st.write(goal.rationale + "\n\n" + goal.visualization)
            i=i+1
        
      

        
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
                library = "seaborn"
                charts = lida.visualize(summary=summary, goal=user_query, textgen_config=textgen_config, library=library)  
                charts[0]
                image_base64 = charts[0].raster
                img = base64_to_image(image_base64)
                st.image(img)
            


