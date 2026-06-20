import json
import time
import requests
import websocket

class GmailTestSender:
    def __init__(self, debug_port=9222):
        self.debug_url = f"http://localhost:{debug_port}/json"
        self.ws = None
        self.msg_id = 0

    def connect_and_verify_gmail(self):
        """Step 1: Check for Gmail tab. If on a home page or other site, open/redirect to Gmail."""
        try:
            tabs = requests.get(self.debug_url).json()
        except Exception:
            print("[-] ERROR: Could not reach port 9222. Ensure Chromium is running in debug mode.")
            return False

        target_tab = None
        
        # 1. First, check if a Gmail tab already exists anywhere
        for tab in tabs:
            if tab.get("type") == "page" and "mail.google.com" in tab.get("url", ""):
                target_tab = tab
                break

        # 2. If no Gmail tab exists, find the active user browser window/tab
        if not target_tab:
            for tab in tabs:
                if tab.get("type") == "page" and "webSocketDebuggerUrl" in tab:
                    target_tab = tab
                    if "newtab" in tab.get("url", "") or "google.com" in tab.get("url", ""):
                        break

        if not target_tab:
            print("[-] ERROR: No active browser page found to attach to.")
            return False

        ws_url = target_tab["webSocketDebuggerUrl"]
        print(f"[+] Connecting to browser tab. Current URL: {target_tab.get('url')}")
        self.ws = websocket.create_connection(ws_url)

        # Force navigation if the current page isn't Gmail
        if "mail.google.com" not in target_tab.get("url", ""):
            print("[*] Redirecting current browser tab to Gmail...")
            self.send_cdp_command("Page.navigate", {"url": "https://mail.google.com"})
            print("[*] Waiting 7 seconds for Gmail dashboard layout to fully render...")
            time.sleep(7)
        else:
            print("[+] Already on Gmail.")
            
        return True

    def send_cdp_command(self, method, params=None):
        if params is None:
            params = {}
        self.msg_id += 1
        payload = {"id": self.msg_id, "method": method, "params": params}
        self.ws.send(json.dumps(payload))

        while True:
            response = json.loads(self.ws.recv())
            if response.get("id") == self.msg_id:
                return response

    def execute_js(self, script):
        response = self.send_cdp_command("Runtime.evaluate", {"expression": script, "returnByValue": True})
        try:
            return response["result"]["result"]["value"]
        except Exception:
            return response

    def trigger_compose_window(self):
        """Step 2: Press the Compose Button."""
        print("[*] Locating and clicking 'Compose' button...")
        compose_js = """
        (() => {
            let composeBtn = document.querySelector('div[role="button"][gh="cm"]') || 
                             document.querySelector('.T-I.T-I-KE.L3');
            
            if (!composeBtn) {
                const buttons = document.querySelectorAll('div[role="button"]');
                for (let btn of buttons) {
                    if (btn.textContent && btn.textContent.trim() === 'Compose') {
                        composeBtn = btn;
                        break;
                    }
                }
            }

            if (composeBtn) {
                composeBtn.focus();
                composeBtn.click();
                return "SUCCESS_COMPOSE_CLICKED";
            }
            return "ERROR_COMPOSE_NOT_FOUND";
        })()
        """
        return self.execute_js(compose_js)

    def write_email(self, recipient, subject, body):
        """Step 3: Populate email using text insertion commands."""
        print(f"[*] Injecting recipient address: {recipient}...")
        
        populate_script = f"""
        (() => {{
            let toField = document.querySelector('input[peoplekit-id], textarea[aria-label="To"], input[aria-label="To"], textarea[name="to"]');
            if (!toField) {{
                const targets = document.querySelectorAll('textarea, input');
                for (let f of targets) {{
                    let lbl = f.getAttribute('aria-label');
                    if (lbl && lbl.toLowerCase().includes('to')) {{ toField = f; break; }}
                }}
            }}
            if (!toField) return "FAILED_TO_FIND_RECIPIENT_FIELD";

            toField.focus();
            document.execCommand('insertText', false, '{recipient}');
            toField.dispatchEvent(new KeyboardEvent('keydown', {{ bubbles: true, cancelable: true, key: 'Enter', keyCode: 13 }}));

            let subjField = document.querySelector('input[name="subjectbox"], input[aria-label="Subject"]');
            if (subjField) {{
                subjField.focus();
                document.execCommand('insertText', false, '{subject}');
            }}

            let bodyField = document.querySelector('div[role="textbox"][aria-label="Message Body"]');
            if (bodyField) {{
                bodyField.focus();
                document.execCommand('insertText', false, '{body}');
            }}

            return "SUCCESS_EMAIL_COMPOSED";
        }})()
        """
        return self.execute_js(populate_script)

    def transmit_email(self):
        """Step 4: Locate the Send button or dispatch the send shortcut."""
        print("[*] Attempting to transmit email...")
        send_script = """
        (() => {
            // Option 1: Find the text box and issue the standard shortcut (Ctrl+Enter)
            let bodyField = document.querySelector('div[role="textbox"][aria-label="Message Body"]');
            if (bodyField) {
                bodyField.focus();
                // Find and click the explicit Send button by its visible attribute or class matching rules
                let sendBtn = document.querySelector('div[role="button"][data-tooltip*="Send"]') || 
                              document.querySelector('.T-I.J-J5-Ji.aoO.v7.T-I-atl.L3');
                
                if (sendBtn) {
                    sendBtn.click();
                    return "SUCCESS_EMAIL_SENT_VIA_CLICK";
                }
            }
            return "ERROR_SEND_BUTTON_NOT_FOUND";
        })()
        """
        return self.execute_js(send_script)

def main():
    sender = GmailTestSender()
    
    # Step 1: Handle browser tab matching and URL redirection
    if not sender.connect_and_verify_gmail():
        return

    # Step 2: Open compose popup
    status = sender.trigger_compose_window()
    print(f"[Compose Click Result]: {status}")
    if status != "SUCCESS_COMPOSE_CLICKED":
        print("[-] Compose window could not be opened.")
        return

    # Short delay to allow compose window opening animations to complete
    time.sleep(2.5)

    # Step 3: Populate details
    recipient = "realmetabforvar@gmail.com"
    subject = "Automated Email Test"
    body = "Success! This email was completely opened, composed, and sent automatically via browser automation scripts."

    composition_status = sender.write_email(recipient, subject, body)
    print(f"[Composition Result]: {composition_status}")
    
    if composition_status == "SUCCESS_EMAIL_COMPOSED":
        # Give the UI 1.5 seconds to settle down after typing
        time.sleep(1.5)
        
        # Step 4: Transmit/Send the email
        send_status = sender.transmit_email()
        print(f"[Send Action Result]: {send_status}")

if __name__ == "__main__":
    main()