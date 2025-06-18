Lida-alternative-project

This project combines Microsoft LIDA with a ChatGPT-driven workflow for interactive data visualization. The goal is to create initial visualizations with LIDA and then further edit them via natural language using ChatGPT.
🧠 Project Idea & Structure

    lida_app.py: This file uses the original functionality of Microsoft LIDA, but adapted to our own custom UI design.

    app.py: This file re-implements the LIDA logic. Here, ChatGPT is used to make modifications to existing charts.

    chatgpt_client.py: Provides functions to communicate with the OpenAI API. This is where prompt engineering happens.

Workflow:

    The first chart is generated using LIDA (lida_app.py or internally via app.py).

    Changes to the chart (e.g., color, axes, filters) are performed through ChatGPT and natural language input.

📁 Project Structure

    app.py – Our main app with GPT-driven visualization

    lida_app.py – LIDA interface with a new UI

    chatgpt_client.py – GPT communication module (formerly test2.py)

    requirements.txt – Dependencies

    README.md – This file

    demo_notebook.ipynb – Initial tests and experiments to better understand LIDA and its limitations

    *.csv – Temporary CSV files provided by the user to the program (not included on GitHub due to .gitignore)

⚙️ Setup Instructions
1. Install Anaconda

If you don’t have it yet:
👉 https://www.anaconda.com/products/distribution
2. Create a new Conda environment

conda create -n chatgpt-vis python=3.11
conda activate chatgpt-vis

3. Install project dependencies

pip install notebook
pip install ipywidgets
pip install python-dotenv
pip install IPython
pip install streamlit
pip install streamlit-audiorecorder
pip install openai
pip install lida

Note: The order is important if you encounter version conflicts with ipywidgets or streamlit.
4. Install FFmpeg (only required for speech functionality)

If you want to use the speech-to-text feature (via streamlit-audiorecorder), you must install FFmpeg (if you don’t want to use speech-to-text, remove it from app.py):

    Download FFmpeg for Windows here:
    👉 https://www.gyan.dev/ffmpeg/builds/

    Extract the folder and add the bin folder to your system PATH environment variable (on Windows).

Without FFmpeg, audio recording will not work, but the app will still run.
5. Set OpenAI API key

Create a .env file in the project directory with the following content:

OPENAI_API_KEY=your-api-key

Alternatively, set it in your terminal:

export OPENAI_API_KEY='your-api-key'

(If you are using Windows: set OPENAI_API_KEY=...)
6. Start the application

streamlit run app.py

Or — to see the original LIDA behavior:

streamlit run lida_app.py