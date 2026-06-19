YOUTUBE_PROMPT = """
==================================================

7. youtube

Functions:

* search
* play_first
* pause
* resume
* get_title
* subscribe
* comment

Arguments for comment:
{
  "text": "your comment string"
}

Examples:

User:
Subscribe to this channel

Output:
{
"tool":"youtube",
"function":"subscribe",
"arguments":{}
}

User:
Comment nice video on youtube

Output:
{
"tool":"youtube",
"function":"comment",
"arguments":{
    "text": "nice video"
}
}
"""