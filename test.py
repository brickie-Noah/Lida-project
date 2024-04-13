# Visualization manager class that handles the visualization of the data with the following methods

# summarize data given a df
# generate goals given a summary
# generate generate visualization specifications given a summary and a goal
# execute the specification given some data

import os
from typing import List, Union
import logging

import pandas as pd
from llmx import llm, TextGenerator
from lida.datamodel import Goal, Summary, TextGenerationConfig, Persona
from lida.utils import read_dataframe
from ..components.summarizer import Summarizer
from ..components.goal import GoalExplorer
from ..components.persona import PersonaExplorer
from ..components.executor import ChartExecutor
from ..components.viz import VizGenerator, VizEditor, VizExplainer, VizEvaluator, VizRepairer, VizRecommender

import lida.web as lida


logger = logging.getLogger("lida")


class Manager(object):
    def summarize(
            self,
            data: Union[pd.DataFrame, str],
            file_name="",
            n_samples: int = 3,
            summary_method: str = "default",
            textgen_config: TextGenerationConfig = TextGenerationConfig(n=1, temperature=0),
        ) -> Summary:
            """
            Summarize data given a DataFrame or file path.

            Args:
                data (Union[pd.DataFrame, str]): Input data, either a DataFrame or file path.
                file_name (str, optional): Name of the file if data is loaded from a file path. Defaults to "".
                n_samples (int, optional): Number of summary samples to generate. Defaults to 3.
                summary_method (str, optional): Summary method to use. Defaults to "default".
                textgen_config (TextGenerationConfig, optional): Text generation configuration. Defaults to TextGenerationConfig(n=1, temperature=0).

            Returns:
                Summary: Summary object containing the generated summary.

            Example of Summary:

                {'name': 'cars.csv',
                'file_name': 'cars.csv',
                'dataset_description': '',
                'fields': [{'column': 'Name',
                'properties': {'dtype': 'string',
                    'samples': ['Nissan Altima S 4dr',
                    'Mercury Marauder 4dr',
                    'Toyota Prius 4dr (gas/electric)'],
                    'num_unique_values': 385,
                    'semantic_type': '',
                    'description': ''}},
                {'column': 'Type',
                'properties': {'dtype': 'category',
                    'samples': ['SUV', 'Minivan', 'Sports Car'],
                    'num_unique_values': 5,
                    'semantic_type': '',
                    'description': ''}},
                {'column': 'AWD',
                'properties': {'dtype': 'number',
                    'std': 0,
                    'min': 0,
                    'max': 1,
                    'samples': [1, 0],
                    'num_unique_values': 2,
                    'semantic_type': '',
                    'description': ''}},
                }

            """
            self.check_textgen(config=textgen_config)

            if isinstance(data, str):
                file_name = data.split("/")[-1]
                data = read_dataframe(data)

            self.data = data
            return self.summarizer.summarize(
                data=self.data, text_gen=self.text_gen, file_name=file_name, n_samples=n_samples,
                summary_method=summary_method, textgen_config=textgen_config)
