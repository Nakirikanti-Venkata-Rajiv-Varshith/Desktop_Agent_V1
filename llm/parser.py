from pydantic import BaseModel, Field
from typing import List, Optional, Literal
import json
from tools.logger import agent_logger

class ActionItem(BaseModel):
    action: Literal["open_app", "open_url", "search"]
    app: Optional[str] = None
    url: Optional[str] = None
    query: Optional[str] = None

class ActionPlanSchema(BaseModel):
    actions: List[ActionItem] = Field(default_factory=list)

class PlanParser:
    """Validates structural accuracy of incoming generation outputs via Pydantic."""
    
    @staticmethod
    def parse_and_validate(raw_text: str) -> ActionPlanSchema:
        """Coerces generation string patterns into validated Pydantic model state."""
        cleaned = raw_text.strip()
        # Edge case cleanup for models that break structural rules and add code fences
        if cleaned.startswith("```"):
            cleaned = cleaned.strip("`").replace("json", "", 1).strip()
            
        try:
            parsed_json = json.loads(cleaned)
            validated_plan = ActionPlanSchema(**parsed_json)
            return validated_plan
        except Exception as e:
            agent_logger.error(f"Pydantic Validation failed for layout: {raw_text}. Error: {str(e)}")
            raise ValueError("LLM response violated structural schema criteria constraints.")