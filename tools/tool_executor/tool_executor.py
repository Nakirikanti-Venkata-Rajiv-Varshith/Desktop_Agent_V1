from tools.system_tools.system_tool import SystemTool
from tools.browser_tools.browser_tool import BrowserTool
from tools.file_tools.file_tool import FileTool
from tools.app_tools.app_tool import AppTool
from tools.chat_tools.chat_tool import ChatTool
from tools.gui_tools.gui_tool import GUITool

class ToolExecutor:

    def execute(
        self,
        tool,
        function,
        arguments
    ):

        tool_map = {
            "system": SystemTool,
            "browser": BrowserTool,
            "file": FileTool,
            "app": AppTool,
            "chat": ChatTool,
            "gui": GUITool
        }

        tool_class = tool_map.get(tool)

        if not tool_class:
            raise ValueError(
                f"Unknown tool: {tool}"
            )

        try:

            fn = getattr(
                tool_class,
                function
            )

        except AttributeError:

            raise ValueError(
                f"Unknown function '{function}' for tool '{tool}'"
            )

        return fn(**arguments)