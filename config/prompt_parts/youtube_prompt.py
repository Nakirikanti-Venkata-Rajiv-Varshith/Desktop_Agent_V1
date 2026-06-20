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
* skip_forward
* skip_backward
* skip_ad

Arguments for comment:
{
  "text": "your comment string"
}

Arguments for skip_forward:
{
  "seconds": integer (Calculate total seconds. e.g., "30s" = 30, "1 min" = 60, "2 min 10s" = 130)
}

Arguments for skip_backward:
{
  "seconds": integer (Calculate total seconds. e.g., "50s" = 50, "3 min" = 180)
}

Arguments for skip_ad:
{}

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

User:
Skip 30 seconds forward

Output:
{
"tool":"youtube",
"function":"skip_forward",
"arguments":{
    "seconds": 30
}
}

User:
Fast forward 3 minutes

Output:
{
"tool":"youtube",
"function":"skip_forward",
"arguments":{
    "seconds": 180
}
}

User:
Go back 50 seconds

Output:
{
"tool":"youtube",
"function":"skip_backward",
"arguments":{
    "seconds": 50
}
}

User:
Rewind 1 and a half minutes

Output:
{
"tool":"youtube",
"function":"skip_backward",
"arguments":{
    "seconds": 90
}
}

User:
Skip this ad

Output:
{
"tool":"youtube",
"function":"skip_ad",
"arguments":{}
}

User:
Clear the commercial breakdown

Output:
{
"tool":"youtube",
"function":"skip_ad",
"arguments":{}
}
"""