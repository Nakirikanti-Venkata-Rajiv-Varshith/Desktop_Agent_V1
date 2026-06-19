from pydantic import BaseModel
from planner.tool_plan import ToolPlan

class TaskPlan(BaseModel):

    steps: list[ToolPlan]