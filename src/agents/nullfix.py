# src/agents/nullfix.py

import os
import logging
from utils import read_yaml
from agents.agent import Agent
from agents.fixerpro import FixerPro
from retry import retry

class NullFix(Agent):
    """
    NullFix places `@Nullable` annotations by incorporating context and error feedback.
    It builds on `FixerPro` but adjusts placements based on error feedback.
    """

    def __init__(self):
        super().__init__()
        self.fixerPro = FixerPro()
        self.training_data = []

    def parse_response(self, response: str):
        """
        Parse the response from LLM to extract annotated code.

        :param response: str, raw response from LLM
        :return: str, code with nullable annotations
        """
        return response.strip() if response else ""

    def generate_prompt(self, code_segment, context, solution_report):
        """
        Generate a prompt for LLM to apply @Nullable annotations.

        :param code_segment: str, problematic code
        :param context: str, additional nullable context
        :param solution_report: str, recommended solutions
        :return: str, generated prompt
        """
        prompt = f"Apply @Nullable annotations to the following code based on the context:\n{code_segment}\n"
        prompt += f"Context:\n{context}\nSolution Report:\n{solution_report}\n"
        return prompt

    @retry((RetryError,), tries=3, delay=5)
    def place_annotations(self, code_segment: str, context: str, solution_report: str):
        """
        Place `@Nullable` annotations using context and solution report.

        :param code_segment: str, code to analyze
        :param context: str, nullable context
        :param solution_report: str, solution insights
        :return: str, annotated code
        """
        logging.info("## Running NullFix to place @Nullable annotations...")
        
        # Load prompts and generate LLM message
        self.prompts_dict = read_yaml(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../prompts/nullfix.yaml"))
        prompt = self.generate_prompt(code_segment, context, solution_report)

        response = self.send_message([
            {"role": "system", "content": self.prompts_dict["sys"]},
            {"role": "user", "content": prompt + "\n" + self.prompts_dict["end"]}
        ])
        
        return self.parse_response(response)

    def train(self, null_away, slicer, null_focus):
        """
        Trains NullFix based on feedback from NullAway, using slices and nullable contexts.

        :param null_away: NullAway instance to detect nullability issues
        :param slicer: Slicer for extracting relevant code slices
        :param null_focus: NullFocus for gathering context
        """
        logging.info("## Training NullFix with collected data...")
        
        warnings = null_away.getWarnings()
        for warning in warnings:
            code_slice = slicer.getCodeSlice(warning)
            context = null_focus.getContext(warning)["context"]
            solution_report = "Initial training solution analysis"

            annotated_code = self.place_annotations(code_slice, context, solution_report)
            null_away.run()
            new_warnings = null_away.getWarnings()

            self.training_data.append((code_slice, context, annotated_code, new_warnings))
            self.fixerPro.fineTune(self.training_data)
