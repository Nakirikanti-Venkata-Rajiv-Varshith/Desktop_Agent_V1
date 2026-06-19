YOUTUBE_PROMPT = """
==================================================

7. youtube

Functions:

* search
* play_first
* pause
* resume
* get_title

Examples:

User:
 open youtube

Output:

{
  "tool":"youtube",
  "function":"open",
  "arguments":{}
}


User:
Search agentic ai on youtube

Output:

{
"tool":"youtube",
"function":"search",
"arguments":{
    "query":"agentic ai"
}
}

User:
Play first video

Output:

{
"tool":"youtube",
"function":"play_first",
"arguments":{}
}

User:
Pause video

Output:

{
"tool":"youtube",
"function":"pause",
"arguments":{}
}

User:
Resume video

Output:

{
"tool":"youtube",
"function":"resume",
"arguments":{}
}

User:
What video is playing?

Output:

{
"tool":"youtube",
"function":"get_title",
"arguments":{}
}
}
"""