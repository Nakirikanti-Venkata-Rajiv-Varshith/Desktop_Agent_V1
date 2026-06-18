EXAMPLES_PROMPT = """
==================================================

EXAMPLE 1

User:
Open Chrome

Output:

{
"tool":"app",
"function":"open",
"arguments":{
"app":"chrome"
}
}

==================================================

EXAMPLE 2

User:
Search latest AI news

Output:

{
"tool":"browser",
"function":"search",
"arguments":{
"query":"latest AI news"
}
}

==================================================

EXAMPLE 3

User:
Open youtube.com

Output:

{
"tool":"browser",
"function":"open_url",
"arguments":{
"url":"https://youtube.com"
}
}

==================================================

EXAMPLE 4

User:
What time is it?

Output:

{
"tool":"system",
"function":"current_time",
"arguments":{}
}

==================================================

EXAMPLE 5

User:
What is today's date?

Output:

{
"tool":"system",
"function":"current_date",
"arguments":{}
}

==================================================

EXAMPLE 6

User:
Show CPU usage

Output:

{
"tool":"system",
"function":"cpu_usage",
"arguments":{}
}

==================================================

EXAMPLE 7

User:
Show files in Downloads

Output:

{
"tool":"file",
"function":"list_directory",
"arguments":{
"path":"~/Downloads"
}
}

==================================================

EXAMPLE 8

User:
How are you?

Output:

{
  "tool":"chat",
  "function":"respond",
  "arguments":{
      "message":"I'm doing well. How can I help?"
  }
}
"""