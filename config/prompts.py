from config.prompt_parts.base_prompt import BASE_PROMPT
from config.prompt_parts.app_prompt import APP_PROMPT
from config.prompt_parts.browser_prompt import BROWSER_PROMPT
from config.prompt_parts.system_prompt import SYSTEM_TOOL_PROMPT
from config.prompt_parts.file_prompt import FILE_PROMPT
from config.prompt_parts.chat_prompt import CHAT_PROMPT
from config.prompt_parts.gui_prompt import GUI_PROMPT
from config.prompt_parts.examples_prompt import EXAMPLES_PROMPT


SYSTEM_PROMPT = "\n".join([
    BASE_PROMPT,
    APP_PROMPT,
    BROWSER_PROMPT,
    SYSTEM_TOOL_PROMPT,
    FILE_PROMPT,
    CHAT_PROMPT,
    GUI_PROMPT,
    EXAMPLES_PROMPT
])