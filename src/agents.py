from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
from pydantic import BaseModel, Field

class CodeError(BaseModel):
    """Structured representation of identified code errors"""
    #error_id: str
    error_description: str = Field(
        description="The description for the error")
    code_snippet: str = Field(
        description="Location of the error in the code")
    topics_quary: List[str] = Field(
        default_factory=list,
        description="List of key words extracted of the error for related topics searching")
    priority: int = Field(
        description="Mark the priority of this error with 1-5. Give larger number to logically prior error or easier error.")
class ErrorList(BaseModel):
    errorList: List[CodeError] = Field(description="The list for all code errors") 

class CodeAnalysisAgent:
    """Identifies and categorizes errors in student code"""

    def __init__(self, client, model: str, CourseSummary):
        """
        Initialize the agent.
        
        Args:
            model_choice: 
        """
        self.client=client 
        self.model = model

        #TODO: Integrate system prompt with CourseSummary 
        #TODO: Refine the system prompt (See *_prompt.txt)

        self.prompt_CodeProcessing=""
    
    
    def detect_errors(self, code: str) -> List[CodeError]:
        """
        Error detection using LLM
        
        Args:
            code: Raw student code input
            
        Returns:
            Structured errors with topic associations
        """

        response = self.client.beta.chat.completions.parse(
        model=self.model,
        n=1,
        messages=[
            {
                "role": "system", 
                "content": self.prompt_CodeProcessing},
            {
                "role": "user",
                "content": code}
        ],
        response_format=ErrorList
        )
        errorList=response.choices[0].message.parsed.errorList

        errorList.sort(key=lambda error: error.priority)

        return errorList
    

class TutorAgent:
    """Agent that directly interacts with the student to facilitate learning."""
    
    def __init__(self, client, model: str, course_materials_db: Any):
        """
        Initialize the tutor agent.
        
        Args:
            model_choice: 
            course_materials_db: Database or retrieval system for course materials
        """
        self.client=client 
        self.model = model

        #TODO: Refine the system prompt (See *_prompt.txt)
        self.prompt_TutorRespond=""
    

    def generate_respond(self, current_error: CodeError, course_material) :
        """
        Generates respond for current error in dialogue. 

        Args: 
            current_error
            course_material

        Returns: 

        """
        #TODO: Integrate system prompt with error information
        prompt_currentError=current_error.error_description

        response = self.client.chat.completions.create(
            model=self.model,
            n=1,
            messages=[
            {
                "role": "system", 
                "content": self.prompt_TutorRespond},
            {
                "role": "user",
                "content": prompt_currentError}
        ]
        )
        response_text = response.choices[0].message.content

        return response_text


class SummaryGenerator:
    """Produces structured learning artifacts"""
    
    @staticmethod
    def generate_session_summary(state: Dict) -> str:
        """
        Creates personalized learning summary
        
        Args:
            state: Current state manager snapshot
            
        Returns:
            Natural language summary with error analysis
        """
        pass

    @staticmethod
    def create_progress_map(state_graph: Dict) -> str:
        """
        Visualizes learning path through curriculum graph
        
        Args:
            state_graph: Complete conversation state structure
            
        Returns:
            Text-based or vector graphic representation
        """
        pass




