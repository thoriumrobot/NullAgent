# src/agents/nullinfer.py

import os
import logging
from utils import read_yaml
from agents.agent import Agent, RetryError
from prompts.tokens import *
from retry import retry

class NullInfer(Agent):
    """
    NullInfer places `@Nullable` annotations in code by analyzing each code segment
    to determine nullable locations. It preserves the original code semantics.
    """

    def parse_response(self, response: str):
        """
        Parse the response to extract the annotated code.

        :param response: str, response from LLM
        :return: str, annotated code with @Nullable placements
        """
        return response.strip() if response else ""

    def __generate_prompt(self, code_segment, summary=None):
        """
        Generate a prompt for LLM to add `@Nullable` annotations.

        :param code_segment: str, the code segment to analyze
        :param summary: str, optional code summary
        :return: str, generated prompt
        """
        prompt = "Analyze the following Java code and add @Nullable annotations where appropriate:\n"
        prompt += f"{code_segment}\n"
        if summary:
            prompt += f"\nSummary of the code:\n{summary}\n"
        return prompt

    @retry((RetryError,), tries=3, delay=5)
    def place_nullable_annotations(self, code_segment: str, summary: str = ""):
        """
        Places `@Nullable` annotations in the code segment.

        :param code_segment: str, the code to annotate
        :param summary: str, optional code summary
        :return: str, annotated code
        """
        logging.info("## Running NullInfer to add @Nullable annotations...")
        
        # Load prompts
        self.prompts_dict = read_yaml(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../prompts/nullinfer.yaml"))
        prompt = self.__generate_prompt(code_segment, summary)

        # Communicate with the LLM for annotation suggestions
        response = self.send_message([
            {"role": "system", "content": self.prompts_dict["sys"]},
            {"role": "user", "content": prompt + "\n" + self.prompts_dict["end"]}
        ])
        
        return self.parse_response(response)
