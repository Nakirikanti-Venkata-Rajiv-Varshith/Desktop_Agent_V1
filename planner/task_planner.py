from llm.ollama_client import OllamaClient
from llm.parser import PlanParser, ActionPlanSchema
from tools.logger import agent_logger

class TaskPlanner:
    """Pipeline component converting natural expressions into structured validation schemas."""
    
    def __init__(self):
        self.client = OllamaClient()
        self.parser = PlanParser()

    def create_plan(self, user_command: str) -> ActionPlanSchema:
        """Processes request strings down through generation and Pydantic confirmation."""
        agent_logger.info(f"Planning requested context: '{user_command}'")
        raw_output = self.client.generate(user_command)
        validated_schema = self.parser.parse_and_validate(raw_output)
        return validated_schema