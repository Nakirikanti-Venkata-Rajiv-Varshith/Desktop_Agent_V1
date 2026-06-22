from pathlib import Path
import ollama

TRANSCRIPT_FILE = "data/gmail_transcript.txt"
LOG_FILE = "logs/gmail_summary.log"

def summarize_emails():

    transcript = Path(
        TRANSCRIPT_FILE
    ).read_text(
        encoding="utf-8"
    )

    prompt = f"""
You are a professional executive email assistant.

You will receive multiple emails.

For EVERY email provide EXACTLY this format:

MAIL 1
Subject: <subject>
Date & Time: <date and time>
Summary: <short summary under 20 words>

MAIL 2
Subject: <subject>
Date & Time: <date and time>
Summary: <short summary under 20 words>

MAIL 3
Subject: <subject>
Date & Time: <date and time>
Summary: <short summary under 20 words>

Continue for all emails found.

After processing all emails create a section:

HIGH PRIORITY EMAILS

Only include emails that are:
- Security alerts
- Banking notifications
- Verification codes
- Job opportunities
- Meeting requests
- Urgent requests
- Deadlines
- Payment related emails
- Account access notifications

Format:

HIGH PRIORITY EMAILS

1.
Subject: <subject>
Date & Time: <date and time>
Reason: <why important>

2.
Subject: <subject>
Date & Time: <date and time>
Reason: <why important>

If there are no important emails write:

HIGH PRIORITY EMAILS

None

Keep summaries concise.

EMAIL DATA:

{transcript}
"""

    response = ollama.chat(
        model="qwen3:8b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    summary = response[
        "message"
    ]["content"]

    Path(
        "logs"
    ).mkdir(
        exist_ok=True
    )

    with open(
        LOG_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(summary)

    print(summary)

    print(
        f"\n[+] Saved summary to {LOG_FILE}"
    )

if __name__ == "__main__":
    summarize_emails()