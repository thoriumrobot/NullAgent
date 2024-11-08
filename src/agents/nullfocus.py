# src/agents/nullfocus.py

import os
import logging
from utils import read_yaml
from agents.agent import Agent

class NullFocus(Agent):
    """
    NullFocus specializes in gathering context for nullability-related issues.
    It examines dependencies, variable usage, and related code segments.
    """

    def gather_dependencies(self, code_segment: str):
        """
        Analyzes the code segment for dependencies.

        :param code_segment: str, code to analyze
        :return: str, dependency context information
        """
        # Here, we use hypothetical methods to parse dependencies (e.g., method or class references)
        # For a real implementation, we could use AST parsing or regex matching
        dependencies = "Dependencies: Analysis of classes, methods, and variables"
        return dependencies

    def generate_prompt(self, code_segment, dependencies):
        """
        Generate a prompt for the LLM to analyze nullability-related context.

        :param code_segment: str, the code with potential nullability issues
        :param dependencies: str, the dependencies related to the code
        :return: str, LLM prompt
        """
        prompt = f"Analyze the following code segment for nullability context:\n{code_segment}\n\n"
        prompt += f"Dependencies:\n{dependencies}\n"
        return prompt

    def get_context(self, warning: dict):
        """
        Retrieves context for a nullability warning.

        :param warning: dict, warning information from NullAway
        :return: dict, context details for nullable analysis
        """
        logging.info("## Running NullFocus to gather context...")
        
        # Retrieve the code segment and its dependencies
        code_segment = warning.get("code_segment", "")
        dependencies = self.gather_dependencies(code_segment)
        
        # Generate prompt for the LLM
        prompt = self.generate_prompt(code_segment, dependencies)
        
        # Send message to the LLM
        response = self.send_message([
            {"role": "system", "content": "Analyze nullability context."},
            {"role": "user", "content": prompt}
        ])
        
        return {"context": response.strip(), "dependencies": dependencies}
