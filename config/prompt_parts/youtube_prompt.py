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
* like
* remove_like

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

User:
Like this video

Output:
{
"tool":"youtube",
"function":"like",
"arguments":{}
}

User:
Give this video a thumbs up

Output:
{
"tool":"youtube",
"function":"like",
"arguments":{}
}

User:
Unlike this video

Output:
{
"tool":"youtube",
"function":"remove_like",
"arguments":{}
}

User:
Remove my like from this video

Output:
{
"tool":"youtube",
"function":"remove_like",
"arguments":{}
}
"""