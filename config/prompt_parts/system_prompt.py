SYSTEM_TOOL_PROMPT = """
==================================================

3. system

Functions:

* current_time
* current_date
* hostname
* os_info
* cpu_usage
* ram_usage
* battery_status
* disk_usage
* ip_address

Arguments:

{}

Examples:

User:
What time is it?

Output:

{
"tool":"system",
"function":"current_time",
"arguments":{}
}

User:
Show CPU usage

Output:

{
"tool":"system",
"function":"cpu_usage",
"arguments":{}
}

User:
What is today's date?

Output:

{
"tool":"system",
"function":"current_date",
"arguments":{}
}
"""