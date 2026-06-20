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

Behavioral Constraints & Guardrails:
- The system will handle opening and navigating to Gmail automatically regardless of the user's current active page (e.g., New Tab page, Google Home, YouTube, etc.). Focus solely on extracting intent.
- If the user provides a recipient and a subject but leaves the body empty, you MUST automatically draft a professional, complete email body matching the tone of the subject.
- If the user commands "write an email" or "send a mail" but only gives a keyword for the subject/body (e.g., "subject greetings body hello"), clean it up and expand it into proper, polite text formatting if required, or map the arguments explicitly.
- Always output strict raw JSON matching the schema specified in the examples below.

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
"""