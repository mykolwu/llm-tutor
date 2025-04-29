from src.agents import CodeError,CodeAnalysisAgent, TutorAgent,SummaryGenerator
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass


class FrontendInterface:
    def send(self, message: str) -> None:
        """
        Send a message (text or structured) to the frontend/UI.
        """
        # TODO: Hook into actual frontend communication
        print(f"Sending to frontend: {message}")

    def receive(self) -> str:
        """
        Receive input from the frontend/UI (e.g., student-submitted code).
        """
        # TODO: Hook into actual frontend communication
        return input("Student code input> ")

@dataclass
class BranchHistory:
    """
    Holds all context for one error-branch:
      - which error it is
      - the stream of messages back and forth
    """
    branch_id: int
    error: CodeError
    messages: List[Message] 


class LLMAgentsWorkflow:
    def __init__(self):
        """
        Perform any startup initialization required for both agents.
        """ 
                
        # TODO: Initialize model clients, load configurations, etc.

        self.code_analyzer = CodeAnalysisAgent()
        self.tutor_agent = TutorAgent()
        self.frontend = FrontendInterface()
        self.errors = []
        #self.current_error_index = 0

        self.historys =[]

    def greet_user(self):
        """
        Send an initial greeting or instructions to the student.
        """
        greeting = (
            "Hello! I'm here to help you debug your code. \n"
            "Please submit your code when you're ready."
        )
        self.frontend.send(greeting)

    def analyze_problem(self, code: str):
        """
        Receive code from the user and analyze it, updating the error list. 
        """
        self.errors = self.code_analyzer.detect_errors(code)

        return None
    
    def initiate_history(self): 
        """
        Creats a separate list of messages for each branch (error).
        """
        pass

    def select_next_branch(self) -> Tuple[BranchHistory, int]:
        pass
    
    def get_history(self, branch_id: int) -> Tuple[BranchHistory, int]:
        pass

    def swich_branch_decision(self) -> bool: 
        pass

    def run_workflow(self):

        # 1) Greeting
        self.frontend.send_message("Hello! Share your code snippet, and I'll help find and explain any issues.")

        # 2) Receive code
        code = self.frontend.receive()

        # 3) Analyze code
        errors = self.analyze_problem(code)
        if not errors:
            self.frontend.send_message("No issues found. Let me know if you have any other questions!")
            return
        self.initiate_history()

        # 4) Create one branch per error
        unresolved = list(errors)
        while unresolved:
            # select which error to process next
            current_branch, branch_id = self.select_next_branch()

            # 5) Process this branch until decision logic says “done”
            while True:

                respond=self.tutor_agent.generate_respond(current_branch)
                self.frontend.send_message(respond, branch_id=branch_id)

                # decide whether to continue on this error
                if not self.swich_branch_decision(): break

        # 6) Wrap up
        self.frontend.send_message("All detected issues have been addressed. Happy coding!")

if __name__ == "__main__":
    workflow = LLMAgentsWorkflow()
    workflow.run()
