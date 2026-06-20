import os
import time
from llm.parser import ToolPlan, TaskPlan
from tools.tool_executor.tool_executor import ToolExecutor
from tools.logger import agent_logger

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

            # 1. Run the tool normally
            result = (
                self.tool_executor.execute(
                    tool=plan.tool,
                    function=plan.function,
                    arguments=plan.arguments
                )
            )

            # 2. FILE INTERCEPTOR STRATEGY:
            # Check if this is our YouTube tool returning a file path success token
            if isinstance(result, dict) and result.get("status") == "SUCCESS" and "saved_to" in result:
                filepath = result["saved_to"]
                if os.path.exists(filepath):
                    try:
                        if status_callback:
                            status_callback("Reading cached transcript file safely into model stream...")
                        
                        # Read the full file contents quietly from storage
                        with open(filepath, "r", encoding="utf-8") as f:
                            transcript_content = f.read()
                        
                        # Overwrite the result payload with a clean template prompt instruction!
                        # When your main agent framework hands this to Ollama, Ollama sees the text seamlessly.
                        result = (
                            f"The user wants a summary or analysis of the active video. "
                            f"The transcript has been successfully extracted from browser cache to disk. "
                            f"Here is the raw transcript context to analyze and answer the user's question:\n\n"
                            f"--- TRANSCRIPT START ---\n{transcript_content}\n--- TRANSCRIPT END ---"
                        )
                    except Exception as fe:
                        agent_logger.error(f"Failed to expand file text data: {str(fe)}")

            # 3. Pass the result back out to the console and caller wrapper
            if status_callback:
                # If it's a huge transcript string, let's just log a small status snippet 
                # so the PyQt6 GUI layout doesn't lag or crash rendering characters!
                if isinstance(result, str) and "--- TRANSCRIPT START ---" in result:
                    status_callback("Transcript loaded successfully. Prompt compiled for Ollama processing.")
                else:
                    status_bar_text = str(result)[:300] + "..." if len(str(result)) > 300 else str(result)
                    status_callback(status_bar_text)

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