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
* set_volume
* increase_volume
* decrease_volume
* set_playback_speed
* set_video_quality

Arguments for set_video_quality:
{
  "quality": string (e.g., "144p", "360p", "720p", "1080p", "highest", "lowest")
}

Arguments for set_playback_speed:
{
  "speed": float (e.g., 1.5, 2.0, 1.0)
}

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

Arguments for set_volume:
{
  "percentage": integer (0 to 100)
}

Arguments for increase_volume:
{
  "current_volume": integer (optional, defaults to 50),
  "step": integer (optional, defaults to 15)
}

Arguments for decrease_volume:
{
  "current_volume": integer (optional, defaults to 50),
  "step": integer (optional, defaults to 15)
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

User:
make it quieter

Output:
{
"tool":"youtube",
"function":"decrease_volume",
"arguments":{
    "step": 25
}
}

User:
turn down the sound a bit

Output:
{
"tool":"youtube",
"function":"decrease_volume",
"arguments":{
    "step": 15
}
}

User:
make it higher

Output:
{
"tool":"youtube",
"function":"increase_volume",
"arguments":{
    "step": 25
}
}

User:
turn up the volume

Output:
{
"tool":"youtube",
"function":"increase_volume",
"arguments":{
    "step": 15
}
}

User:
mute the video

Output:
{
"tool":"youtube",
"function":"set_volume",
"arguments":{
    "percentage": 0
}
}

User:
make it max volume

Output:
{
"tool":"youtube",
"function":"set_volume",
"arguments":{
    "percentage": 100
}
}

User:
set volume to 60 percent

Output:
{
"tool":"youtube",
"function":"set_volume",
"arguments":{
    "percentage": 60
}
}

User:
Watch this tutorial at 2x speed

Output:
{
  "tool": "youtube",
  "function": "set_playback_speed",
  "arguments": {
    "speed": 2.0
  }
}

User:
Change video resolution to 480p to save mobile data balance

Output:
{
  "tool": "youtube",
  "function": "set_video_quality",
  "arguments": {
    "quality": "480p"
  }
}
"""