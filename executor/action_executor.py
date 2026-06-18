from llm.parser import ToolPlan

from tools.tool_executor.tool_executor import ToolExecutor

from tools.logger import agent_logger


class ActionExecutor:

    def __init__(self):

        self.tool_executor = ToolExecutor()

    def execute(
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