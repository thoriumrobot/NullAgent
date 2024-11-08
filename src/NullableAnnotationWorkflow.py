# src/NullableAnnotationWorkflow.py

import logging
from agents.nullaway_annotator import NullAwayAnnotator
from agents.nullinfer import NullInfer
from agents.nullfix import NullFix
from agents.nullfocus import NullFocus
from agents.helper import Helper
from external_tools.nullaway import NullAway
from external_tools.slicer import Slicer
from external_tools.vgr import VGR

class NullableAnnotationWorkflow:
    """
    Manages a multi-level workflow to add `@Nullable` annotations to Java code
    using a series of agents and external tools.
    """

    def __init__(self):
        # Initialize agents and tools
        self.annotator = NullAwayAnnotator()
        self.null_away = NullAway()
        self.vgr = VGR()
        self.slicer = Slicer()
        self.null_infer = NullInfer()
        self.null_focus = NullFocus()
        self.null_fix = NullFix()
        self.helper = Helper()

    def execute(self):
        """
        Executes the multi-level annotation workflow.
        Starts from basic annotation placement and escalates to advanced
        context-driven analysis if warnings persist.
        """
        logging.info("Starting Nullable Annotation Workflow...")
        
        # Level 1: Basic Annotation and Refactoring
        self.level_one()
        
        # Level 2: If warnings remain, introduce deeper analysis with NullInfer
        if self.null_away.hasWarnings():
            self.level_two()
        
        # Level 3: If warnings still remain, use NullFocus and Helper to try advanced solutions
        if self.null_away.hasWarnings():
            self.level_three()

        logging.info("Nullable Annotation Workflow completed.")

    def level_one(self):
        """
        Level 1: Initial placement of `@Nullable` annotations by NullAwayAnnotator
        and basic semantics-preserving refactoring with VGR.
        """
        logging.info("## Level 1: Initial Annotation Placement and Refactoring")

        # Step 1: Place initial annotations using NullAwayAnnotator
        self.annotator.placeInitialAnnotations()
        
        # Step 2: Run NullAway to detect initial warnings
        warnings = self.null_away.getWarnings()
        
        # Step 3: Refactor to resolve warnings while preserving semantics with VGR
        for warning in warnings:
            logging.info(f"Refactoring to address warning: {warning}")
            self.vgr.refactor(warning)
        
        # Re-run NullAway after refactoring to check for remaining issues
        self.null_away.run()

    def level_two(self):
        """
        Level 2: Introduce NullInfer to analyze and place annotations based on
        refined slices and summaries. This preserves semantics.
        """
        logging.info("## Level 2: Deep Analysis with NullInfer")

        # Get remaining warnings from NullAway
        warnings = self.null_away.getWarnings()
        
        for warning in warnings:
            # Step 1: Slice the code around each warning
            code_slice = self.slicer.getCodeSlice(warning)
            
            # Step 2: Generate a summary if the slice is too large
            summary = ""
            if len(code_slice) > 300:  # Adjust threshold based on context
                summary = self.summarizer.summarize(code_slice)
            
            # Step 3: Use NullInfer to place `@Nullable` annotations based on the slice and summary
            annotated_code = self.null_infer.place_nullable_annotations(code_slice, summary)
            
            # Apply the annotations (actual integration would depend on project setup)
            logging.info(f"Annotations applied to code slice:\n{annotated_code}")
        
        # Run NullAway again to verify if annotations resolved warnings
        self.null_away.run()

    def level_three(self):
        """
        Level 3: Advanced annotation with NullFix using deeper nullability context
        provided by NullFocus and solution insights from Helper.
        """
        logging.info("## Level 3: Advanced NullFix and Contextual Analysis")

        warnings = self.null_away.getWarnings()
        
        for warning in warnings:
            # Step 1: Use NullFocus to get deeper null-related context for each warning
            null_context = self.null_focus.get_context(warning)["context"]
            
            # Step 2: Use Helper to search for solutions based on the context
            solution_report = self.helper.searchSolutions(null_context)
            
            # Step 3: Use NullFix to place `@Nullable` annotations with a focus on resolving warnings
            # without preserving semantics (allowing more freedom in fixing).
            annotated_code = self.null_fix.place_annotations(warning["code_segment"], null_context, solution_report)
            
            # Apply the annotations as determined by NullFix
            logging.info(f"Advanced annotations applied by NullFix:\n{annotated_code}")
        
        # Re-run NullAway to confirm if issues have been resolved after NullFix's annotations
        self.null_away.run()

    def train_nullfix(self):
        """
        Optional training loop to further refine NullFix using feedback from NullAway,
        Slicer, and NullFocus.
        """
        logging.info("## Training NullFix with accumulated data")
        
        # Use warnings to collect training data
        warnings = self.null_away.getWarnings()
        for warning in warnings:
            code_slice = self.slicer.getCodeSlice(warning)
            context = self.null_focus.get_context(warning)["context"]
            
            # Train NullFix iteratively to improve annotation accuracy
            self.null_fix.train(self.null_away, self.slicer, self.null_focus)
