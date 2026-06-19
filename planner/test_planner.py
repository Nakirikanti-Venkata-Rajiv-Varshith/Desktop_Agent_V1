from planner.task_planner import TaskPlanner
from tools.tool_executor.tool_executor import ToolExecutor

planner = TaskPlanner()
executor = ToolExecutor()

plan = planner.create_plan(
    "play first video"
)

for step in plan.steps:

    result = executor.execute(
        step.tool,
        step.function,
        step.arguments
    )

    print(result)