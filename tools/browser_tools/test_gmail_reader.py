from pathlib import Path
from datetime import datetime
from playwright.sync_api import sync_playwright

TRANSCRIPT_FILE = "data/gmail_transcript.txt"


def read_emails_by_date(target_date="today"):

    if target_date == "today":
        date_filter = datetime.now().strftime("%b")
    else:
        date_filter = target_date

    with sync_playwright() as p:

        browser = p.chromium.connect_over_cdp(
            "http://localhost:9222"
        )

        context = browser.contexts[0]

        gmail_page = None

        for page in context.pages:
            if "mail.google.com" in page.url:
                gmail_page = page
                break

        if gmail_page is None:
            gmail_page = context.new_page()
            gmail_page.goto(
                "https://mail.google.com"
            )
            gmail_page.wait_for_timeout(8000)

        gmail_page.bring_to_front()

        gmail_page.wait_for_timeout(5000)

        emails = gmail_page.evaluate("""
        () => {

            const rows = Array.from(
                document.querySelectorAll(
                    'tr[role="row"]'
                )
            );

            const collected = [];

            for (const row of rows) {

                try {

                    const sender =
                        row.querySelector('.yP')
                        ?.innerText || '';

                    const subject =
                        row.querySelector('.bog')
                        ?.innerText || '';

                    const snippet =
                        row.querySelector('.y2')
                        ?.innerText || '';

                    const date =
                        row.querySelector('td.xW span')
                        ?.getAttribute('title')
                        ||
                        row.querySelector('td.xW span')
                        ?.innerText
                        ||
                        '';

                    collected.push({
                        sender,
                        subject,
                        snippet,
                        date
                    });

                } catch(err) {}
            }

            return collected;
        }
        """)

        filtered_emails = []

        if target_date == "today":

            today_day = str(
                datetime.now().day
            )

            for mail in emails:

                mail_date = str(
                    mail["date"]
                )

                if today_day in mail_date:
                    filtered_emails.append(
                        mail
                    )

        else:

            for mail in emails:

                if target_date.lower() in str(
                    mail["date"]
                ).lower():

                    filtered_emails.append(
                        mail
                    )

        Path(
            "data"
        ).mkdir(
            exist_ok=True
        )

        with open(
            TRANSCRIPT_FILE,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(
                f"DATE FILTER: {target_date}\n\n"
            )

            for idx, email in enumerate(
                filtered_emails,
                start=1
            ):

                f.write(
                    f"EMAIL {idx}\n"
                )

                f.write(
                    f"Sender: {email['sender']}\n"
                )

                f.write(
                    f"Subject: {email['subject']}\n"
                )

                f.write(
                    f"Snippet: {email['snippet']}\n"
                )

                f.write(
                    f"Date: {email['date']}\n"
                )

                f.write(
                    "\n---------------------------------\n\n"
                )

        print(
            f"[+] Saved {len(filtered_emails)} matching emails"
        )

        print(
            f"[+] Transcript: {TRANSCRIPT_FILE}"
        )


if __name__ == "__main__":

    read_emails_by_date(
        "today"
    )

    # Examples:
    #
    # read_emails_by_date("Jun 20")
    # read_emails_by_date("Jun 21")
    # read_emails_by_date("Jun")