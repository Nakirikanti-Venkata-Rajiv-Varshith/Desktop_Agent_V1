from llm.parser import ToolPlan, TaskPlan
from tools.tool_executor.tool_executor import ToolExecutor
from tools.logger import agent_logger
import time

class ActionExecutor:

    def __init__(self):

        self.tool_executor = ToolExecutor()

    def execute_single(
        self,
        plan: ToolPlan,
        status_callback=None
    ) -> bool:

        try:

            msg = (
                f"Executing Tool: "
                f"{plan.tool}."
                f"{plan.function}"
            )

            agent_logger.info(msg)

            if status_callback:
                status_callback(msg)

            result = (
                self.tool_executor.execute(
                    tool=plan.tool,
                    function=plan.function,
                    arguments=plan.arguments
                )
            )

            if status_callback:
                status_callback(
                    str(result)
                )

            return True

        except Exception as e:

            err_msg = (
                f"Tool Execution Failed: "
                f"{str(e)}"
            )

            agent_logger.error(err_msg)

            if status_callback:
                status_callback(err_msg)

            return False
        
    def execute_task_plan(
        self,
        task_plan: TaskPlan,
        status_callback=None
    ) -> bool:

        overall_success = True

        for step in task_plan.steps:

            success = self.execute_single(
                step,
                status_callback
            )

            overall_success = (
                overall_success and success
            )

            time.sleep(1)

        return overall_success