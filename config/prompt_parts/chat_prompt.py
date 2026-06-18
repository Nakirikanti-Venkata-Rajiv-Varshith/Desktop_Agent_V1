CHAT_PROMPT = """
==================================================

5. chat

Function:

respond

Arguments:

{
"message":"..."
}

Examples:

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

User:
Tell me a joke

Output:

{
"tool":"chat",
"function":"respond",
"arguments":{
"message":"..."
}
}
"""