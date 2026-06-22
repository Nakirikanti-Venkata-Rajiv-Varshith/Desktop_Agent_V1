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

        if tool == "youtube":

            youtube_aliases = {

                "play": "play_first",

                "play_video": "play_first",

                "play_first_video": "play_first",

                "search_video": "search",

                "pause_video": "pause",

                "resume_video": "resume",

                "summary": "get_video_transcript",

                "summarize": "get_video_transcript",

                "summarize_video": "get_video_transcript",

                "video_summary": "get_video_transcript",

                "explain_video": "get_video_transcript",

                "exit": "exit_video",
                "back": "exit_video",
                "go_back": "exit_video",
                "close_video": "exit_video",
                "leave_video": "exit_video",
                "return_to_results": "exit_video",
                "exit_current_video": "exit_video"
            }

            function = youtube_aliases.get(
                function,
                function
            )
            if function == "comment":

                    if "comment" in arguments:
                        arguments["text"] = arguments.pop(
                            "comment"
                        )

            if function == "play_first":
                arguments = {}

            if function == "get_video_transcript":
                arguments = {}



        if tool == "gmail":

            gmail_aliases = {

                # open gmail
                "open_gmail": "open",
                "launch_gmail": "open",

                # compose mail
                "send_email": "compose_email",
                "write_email": "compose_email",
                "draft_email": "compose_email",
                "compose_mail": "compose_email",
                "send_mail": "compose_email",

                # schedule mail
                "schedule_mail": "schedule_email",
                "schedule_send": "schedule_email",
                "send_later": "schedule_email",

                # summarize
                "summarize_mail": "summarize_emails",
                "summarize_mails": "summarize_emails",
                "summarize_email": "summarize_emails",
                "email_summary": "summarize_emails",

                # fetch
                "fetch_mail": "fetch_emails_by_date",
                "fetch_emails": "fetch_emails_by_date",
                "get_emails": "fetch_emails_by_date",
                "read_emails": "fetch_emails_by_date"
            }

            function = gmail_aliases.get(
                function,
                function
            )


        print(
            f"[ToolExecutor] {tool}.{function}"
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