GUI_PROMPT = """
==================================================

6. gui

Functions:

* move_mouse

Arguments:

{
"x":100,
"y":200
}

* click

Arguments:

{}

* double_click

Arguments:

{}

* type_text

Arguments:

{
"text":"hello"
}

* hotkey

Arguments:

{
"keys":["ctrl","t"]
}

* press

Arguments:

{
"key":"enter"
}

Examples:

User:
Press Enter

Output:

{
"tool":"gui",
"function":"press",
"arguments":{
"key":"enter"
}
}

User:
Press Ctrl T

Output:

{
"tool":"gui",
"function":"hotkey",
"arguments":{
"keys":["ctrl","t"]
}
}
"""