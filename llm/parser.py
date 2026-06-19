from pydantic import BaseModel, Field
from typing import List, Optional, Literal
import json
from tools.logger import agent_logger

class ToolPlan(BaseModel):

    tool: str

    function: str

    arguments: dict = Field(default_factory=dict)

class TaskPlan(BaseModel):

    steps: list[ToolPlan]

class PlanParser:
    """Validates structural accuracy of incoming generation outputs via Pydantic."""
    
    @staticmethod
    def parse_and_validate(raw_text: str) -> TaskPlan:
        """Coerces generation string patterns into validated Pydantic model state."""
        cleaned = raw_text.strip()
        # Edge case cleanup for models that break structural rules and add code fences
        if cleaned.startswith("```"):
            cleaned = cleaned.strip("`").replace("json", "", 1).strip()
            
        try:
            parsed_json = json.loads(cleaned)
            if "steps" not in parsed_json:

                parsed_json = {
                    "steps": [
                        parsed_json
                    ]
                }

            validated_plan = TaskPlan(
                **parsed_json
            )

            return validated_plan

            validated_plan = TaskPlan(**parsed_json)
            return validated_plan
        except Exception as e:
            agent_logger.error(f"Pydantic Validation failed for layout: {raw_text}. Error: {str(e)}")
            raise ValueError("LLM response violated structural schema criteria constraints.")