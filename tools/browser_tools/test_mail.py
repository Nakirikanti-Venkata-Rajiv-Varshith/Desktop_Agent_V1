import sys
from datetime import datetime, timedelta
from playwright.sync_api import sync_playwright

def schedule_email_hybrid(recipient, subject, body, target_time_str):
    """
    Uses a hybrid approach:
    1. Uses raw JavaScript injection to flawlessly compose the email.
    2. Uses Playwright's native locators to robustly handle the scheduling UI pop-ups.
    """
    # Calculate target delivery timing context
    now = datetime.now()
    target_time = datetime.strptime(target_time_str, "%H:%M").replace(
        year=now.year, month=now.month, day=now.day
    )
    if target_time <= now:
        target_time += timedelta(days=1)
    
    # Format dates required for the Gmail UI picker (e.g., "June 22, 2026" and "12:00 PM")
    # Use full month name to match Gmail's display.
    target_date_str = target_time.strftime("%B %d, %Y")
    target_hour_str = target_time.strftime("%I:%M %p")

    print(f"[*] Connecting to local Chromium debugging instance on port 9222...")
    
    with sync_playwright() as p:
        try:
            # Connect to your already running open browser session
            browser = p.chromium.connect_over_cdp("http://localhost:9222")
            context = browser.contexts[0]
            
            # Find the active Gmail tab, or open a new one
            gmail_page = next((page for page in context.pages if "mail.google.com" in page.url), None)
            if not gmail_page:
                print("[*] Gmail tab not found. Opening a new tab...")
                gmail_page = context.new_page()
                gmail_page.goto("https://mail.google.com")
                gmail_page.wait_for_timeout(5000)
            
            print("[*] Injecting JS to trigger Compose window...")
            # --- STEP 1: JS Injection to open Compose ---
            gmail_page.evaluate("""
                () => {
                    let composeBtn = document.querySelector('div[role="button"][gh="cm"]') || 
                                     document.querySelector('.T-I.T-I-KE.L3');
                    if (composeBtn) {
                        composeBtn.focus();
                        composeBtn.click();
                    }
                }
            """)
            gmail_page.wait_for_timeout(2000) # Wait for animation
            
            print(f"[*] Injecting JS to populate fields for: {recipient}...")
            # --- STEP 2: JS Injection to fill email fields ---
            gmail_page.evaluate("""
                ([rec, sub, bod]) => {
                    // Fill To field
                    let toField = document.querySelector('input[peoplekit-id], textarea[aria-label="To"], input[aria-label="To"], textarea[name="to"]');
                    if (toField) {
                        toField.focus();
                        document.execCommand('insertText', false, rec);
                        toField.dispatchEvent(new KeyboardEvent('keydown', { bubbles: true, cancelable: true, key: 'Enter', keyCode: 13 }));
                    }

                    // Fill Subject
                    let subjField = document.querySelector('input[name="subjectbox"], input[aria-label="Subject"]');
                    if (subjField) {
                        subjField.focus();
                        document.execCommand('insertText', false, sub);
                    }

                    // Fill Body
                    let bodyField = document.querySelector('div[role="textbox"][aria-label="Message Body"]');
                    if (bodyField) {
                        bodyField.focus();
                        document.execCommand('insertText', false, bod);
                    }
                }
            """, [recipient, subject, body])
            
            gmail_page.wait_for_timeout(2000)
            
            # --- STEP 3: Playwright handles the Scheduling Menus ---
            print("[*] Accessing scheduling dropdown mechanisms via Playwright...")
            
            # Click the dropdown arrow next to 'Send'
            gmail_page.locator('div[role="button"][data-tooltip*="More send options"], .G-asf').first.click()
            gmail_page.wait_for_timeout(1000)
            
            # Click 'Schedule send' in the small menu
            gmail_page.locator('div[role="menuitem"]:has-text("Schedule send")').first.click()
            gmail_page.wait_for_timeout(1500)
            
            # Click 'Pick date & time' in the modal dialog
            gmail_page.locator('text=Pick date & time').first.click()
            
            # Wait for the specific dialogue box from your screenshot to appear
            schedule_dialog = gmail_page.get_by_role(
                "dialog",
                name="Pick date & time"
            )
            schedule_dialog.wait_for(timeout=5000)
            
            # --- STEP 4: Fill the Date and Time fields ---
            print(f"[*] Setting delivery parameter targets: {target_date_str} at {target_hour_str}")

            dialog_inputs = schedule_dialog.locator("input")

            print("========== DIALOG HTML ==========")
            print(schedule_dialog.inner_html())
            print("=================================")

            count = dialog_inputs.count()
            print(f"Found {count} inputs in dialog")

            for i in range(count):
                try:
                    info = dialog_inputs.nth(i).evaluate('''
                    el => ({
                        value: el.value,
                        type: el.type,
                        aria: el.getAttribute('aria-label'),
                        placeholder: el.placeholder
                    })
                    ''')
                    print(f"INPUT {i}: {info}")
                except Exception as e:
                    print(e)

            # DATE FIELD
            date_input = dialog_inputs.nth(0)

            date_input.click()
            gmail_page.keyboard.press("Meta+A" if sys.platform == "darwin" else "Control+A")
            gmail_page.keyboard.type(target_date_str, delay=100)

            # IMPORTANT
            gmail_page.keyboard.press("Tab")

            gmail_page.wait_for_timeout(500)

            # TIME FIELD
            time_input = dialog_inputs.nth(1)

            time_input.click()
            gmail_page.keyboard.press("Meta+A" if sys.platform == "darwin" else "Control+A")
            # Use fill for more reliable input entry
            time_input.fill(target_hour_str)
            time_input.press("Tab")

            gmail_page.wait_for_timeout(1000)

            # Click Schedule Send using the dialog-scoped button
            schedule_dialog.get_by_role(
                "button",
                name="Schedule send"
            ).click()

            gmail_page.wait_for_timeout(3000)
            
            print(f"[+] Success! Mail successfully scheduled natively on Google's timeline.")
            print(f"[!] You can now safely power off your local machine.")
            
        except Exception as error:
            print(f"[-] Hybrid Automation Execution Error: {error}")

if __name__ == "__main__":
    TARGET_RECIPIENT = "realmetabfor@gmail.com"
    TARGET_SUBJECT = "Automated Scheduled Email Test"
    TARGET_BODY = "Hello! This email was composed and scheduled automatically using hybrid browser-automation tools."
    TARGET_TIME = "12:00"  # 24-hour notation string mapping

    schedule_email_hybrid(TARGET_RECIPIENT, TARGET_SUBJECT, TARGET_BODY, TARGET_TIME)