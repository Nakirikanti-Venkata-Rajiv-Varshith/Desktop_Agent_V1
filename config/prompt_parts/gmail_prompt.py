GMAIL_PROMPT = """
==================================================

8. gmail

Functions:

* open
Arguments: {}

* compose_email
Arguments:
{
  "recipient": string (valid target email format),
  "subject": string (clean summary string text. If missing or implicit, dynamically generate a professional subject line),
  "body": string (complete email text content block. If missing, draft a contextually relevant, professional body based on user intent)
}

* schedule_email

Arguments:
{
  "recipient": string,
  "subject": string,
  "body": string,
  "time": string
}

Behavioral Constraints & Guardrails:
- The system will handle opening and navigating to Gmail automatically regardless of the user's current active page (e.g., New Tab page, Google Home, YouTube, etc.). Focus solely on extracting intent.
- If the user provides a recipient and a subject but leaves the body empty, you MUST automatically draft a professional, complete email body matching the tone of the subject.
- If the user commands "write an email" or "send a mail" but only gives a keyword for the subject/body (e.g., "subject greetings body hello"), clean it up and expand it into proper, polite text formatting if required, or map the arguments explicitly.
- Always output strict raw JSON matching the schema specified in the examples below.


IMPORTANT:

If the user mentions ANY future delivery time such as:

- tomorrow
- later
- schedule
- send at
- send tomorrow
- tomorrow morning
- tomorrow evening
- next hour
- at 2 PM
- at 5 PM

then ALWAYS use:

"function":"schedule_email"

and NEVER use:

"function":"compose_email"

Compose_email is ONLY for immediate sending.

Examples:

User:
Open gmail
Output:
{
"tool":"gmail",
"function":"open",
"arguments":{}
}

User:
Send an email to user@example.com saying hello with subject Test
Output:
{
"tool":"gmail",
"function":"compose_email",
"arguments":{
  "recipient":"user@example.com",
  "subject":"Test",
  "body":"Hello,\n\nJust wanted to reach out and say hello. Hope you are doing well!\n\nBest regards."
}
}

User:
write a mail to realmetabforvar@gmail.com subject greetings body hello
Output:
{
"tool":"gmail",
"function":"compose_email",
"arguments":{
  "recipient":"realmetabforvar@gmail.com",
  "subject":"Greetings",
  "body":"Hello,\n\nI am reaching out to send you my best greetings. I hope everything is going well on your end.\n\nBest regards."
}
}

User:
Email test@domain.com about scheduling a sync meeting for tomorrow morning but I don't know what to write in the body
Output:
{
"tool":"gmail",
"function":"compose_email",
"arguments":{
  "recipient":"test@domain.com",
  "subject":"Scheduling Sync Meeting - Tomorrow Morning",
  "body":"Hello,\n\nI would like to schedule a quick sync meeting with you tomorrow morning to review our current progress and align on next steps. Please let me know what time works best for your schedule.\n\nThank you,\nAhead Team"
}
}

User:
Mail boss@company.com subject Urgent Update
Output:
{
"tool":"gmail",
"function":"compose_email",
"arguments":{
  "recipient":"boss@company.com",
  "subject":"Urgent Update",
  "body":"Hello,\n\nI am writing to provide you with an urgent update regarding our ongoing operations. Please let me know when you have a moment to review this or discuss further.\n\nBest regards."
}
}

User:
Send an email to user@example.com saying Namaste and schedule it for 1 PM

Output:
{
  "tool":"gmail",
  "function":"schedule_email",
  "arguments":{
    "recipient":"user@example.com",
    "subject":"Greeting",
    "body":"Namaste",
    "time":"13:00"
  }
}

User:
Send a mail to zforvar@gmail.com subject Hello body Namaste tomorrow at 2 PM

Output:
{
  "tool":"gmail",
  "function":"schedule_email",
  "arguments":{
    "recipient":"zforvar@gmail.com",
    "subject":"Hello",
    "body":"Namaste",
    "time":"14:00"
  }
}

User:
Email abc@gmail.com tomorrow 5 PM subject Meeting Reminder body Don't forget the meeting

Output:
{
  "tool":"gmail",
  "function":"schedule_email",
  "arguments":{
    "recipient":"abc@gmail.com",
    "subject":"Meeting Reminder",
    "body":"Don't forget the meeting",
    "time":"17:00"
  }
}

User:
Schedule an email to john@gmail.com at 9 AM tomorrow saying Good Morning

Output:
{
  "tool":"gmail",
  "function":"schedule_email",
  "arguments":{
    "recipient":"john@gmail.com",
    "subject":"Good Morning",
    "body":"Good Morning",
    "time":"09:00"
  }
}

User:
Send a mail later today at 6 PM to test@gmail.com subject Status Update body Project completed

Output:
{
  "tool":"gmail",
  "function":"schedule_email",
  "arguments":{
    "recipient":"test@gmail.com",
    "subject":"Status Update",
    "body":"Project completed",
    "time":"18:00"
  }
}

User:
Send an email to user@example.com subject Test body Hello

Output:
{
  "tool":"gmail",
  "function":"compose_email",
  "arguments":{
    "recipient":"user@example.com",
    "subject":"Test",
    "body":"Hello"
  }
}

User:
Compose mail to xxx@gmail.com subject Hello body How are you and schedule this for tomorrow 2 PM

Output:
{
  "tool":"gmail",
  "function":"schedule_email",
  "arguments":{
    "recipient":"xxx@gmail.com",
    "subject":"Hello",
    "body":"How are you",
    "time":"14:00"
  }
}

User:
Write an email to abc@gmail.com subject Greetings body Namaste and send it tomorrow at 9 AM

Output:
{
  "tool":"gmail",
  "function":"schedule_email",
  "arguments":{
    "recipient":"abc@gmail.com",
    "subject":"Greetings",
    "body":"Namaste",
    "time":"09:00"
  }
}

User:
Compose an email to test@gmail.com saying hello and schedule it for 5 PM

Output:
{
  "tool":"gmail",
  "function":"schedule_email",
  "arguments":{
    "recipient":"test@gmail.com",
    "subject":"Hello",
    "body":"Hello",
    "time":"17:00"
  }
}

User:
Draft a mail to boss@company.com subject Project Update body Work completed and schedule for tomorrow evening

Output:
{
  "tool":"gmail",
  "function":"schedule_email",
  "arguments":{
    "recipient":"boss@company.com",
    "subject":"Project Update",
    "body":"Work completed",
    "time":"18:00"
  }
}

User:
Mail xyz@gmail.com tomorrow 3 PM subject Reminder body Meeting starts at 4

Output:
{
  "tool":"gmail",
  "function":"schedule_email",
  "arguments":{
    "recipient":"xyz@gmail.com",
    "subject":"Reminder",
    "body":"Meeting starts at 4",
    "time":"15:00"
  }
}

User:
Create an email for abc@gmail.com subject Status body Task completed and schedule delivery for tomorrow at 11 AM

Output:
{
  "tool":"gmail",
  "function":"schedule_email",
  "arguments":{
    "recipient":"abc@gmail.com",
    "subject":"Status",
    "body":"Task completed",
    "time":"11:00"
  }
}
"""