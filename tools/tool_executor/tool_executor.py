from system_tools.system_tool import SystemTool
from browser_tools.browser_tool import BrowserTool
from file_tools.file_tool import FileTool
from app_tools.app_tool import AppTool

class ToolExecutor:

    def execute(
        self,
        tool,
        function,
        arguments
    ):

        if tool == "system":

            fn = getattr(
                SystemTool,
                function
            )

            return fn(**arguments)

        elif tool == "browser":

            fn = getattr(
                BrowserTool,
                function
            )

            return fn(**arguments)

        elif tool == "file":

            fn = getattr(
                FileTool,
                function
            )

            return fn(**arguments)

        elif tool == "app":

            fn = getattr(
                AppTool,
                function
            )

            return fn(**arguments)