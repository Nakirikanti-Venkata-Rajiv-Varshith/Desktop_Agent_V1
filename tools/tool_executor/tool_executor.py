from tools.system_tools.system_tool import SystemTool
from tools.browser_tools.browser_tool import BrowserTool
from tools.file_tools.file_tool import FileTool
from tools.app_tools.app_tool import AppTool
from tools.chat_tools.chat_tool import ChatTool
from tools.gui_tools.gui_tool import GUITool
from tools.browser_tools.youtube_tool import YouTubeTool
from tools.browser_tools.gmail_tool import GmailTool

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
            "gui": GUITool,
            "youtube": YouTubeTool,
            "gmail": GmailTool
        }

        tool_class = tool_map.get(tool)

        if not tool_class:
            raise ValueError(
                f"Unknown tool: {tool}"
            )

        # Instantiate browser-based automation classes that manage active state sessions
        if tool in ["youtube", "gmail"]:
            tool_class = tool_class()

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