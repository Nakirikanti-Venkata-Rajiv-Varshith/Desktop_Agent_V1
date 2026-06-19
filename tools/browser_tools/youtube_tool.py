from tools.browser_tools.cdp_client import CDPClient
import webbrowser
import time
import subprocess

class YouTubeTool:

    def __init__(self):
        self.client = CDPClient()
        self.client.connect()

    @staticmethod
    def open():
        user_profile_dir = "/home/varshith-nakirikanti/snap/chromium/common/chromium"

        subprocess.Popen([
            "chromium",
            "--remote-debugging-port=9222",
            "--remote-allow-origins=*",
            f"--user-data-dir={user_profile_dir}",
            "https://youtube.com"
        ])

        return "YouTube Opened"

    def pause(self):
        return self.client.send(
            "Runtime.evaluate",
            {
                "expression": """
                (() => {
                    const video = document.querySelector('video');
                    if (!video) return "NOT_FOUND";
                    video.pause();
                    return "PAUSED";
                })()
                """,
                "returnByValue": True
            }
        )
    
    def resume(self):
        return self.client.send(
            "Runtime.evaluate",
            {
                "expression": """
                (() => {
                    const video = document.querySelector('video');
                    if (!video) return "NOT_FOUND";
                    video.play();
                    return "PLAYING";
                })()
                """,
                "returnByValue": True
            }
        )
    
    def get_title(self):
        return self.client.execute_js("document.title")

    def search(self, query):
        js = f"""
        (() => {{
            const input = document.querySelector('input[name="search_query"]');
            if (!input) return "SEARCH_BOX_NOT_FOUND";

            input.focus();
            input.value = "{query}";

            input.dispatchEvent(
                new InputEvent(
                    "input",
                    {{ bubbles: true, composed: true }}
                )
            );

            input.dispatchEvent(
                new KeyboardEvent(
                    "keydown",
                    {{
                        key: "Enter",
                        code: "Enter",
                        keyCode: 13,
                        which: 13,
                        bubbles: true
                    }}
                )
            );

            return "SEARCH_TRIGGERED";
        }})()
        """
        return self.client.send(
            "Runtime.evaluate",
            {
                "expression": js,
                "returnByValue": True
            }
        )

    def play_first(self):
        nav_result = self.client.send(
            "Runtime.evaluate",
            {
                "expression": """
                (() => {
                    const firstVideo = document.querySelector('ytd-video-renderer a#video-title');
                    if (!firstVideo) return "VIDEO_NOT_FOUND";
                    window.location = firstVideo.href;
                    return firstVideo.href;
                })()
                """,
                "returnByValue": True
            }
        )

        val = nav_result.get("result", {}).get("result", {}).get("value", "")
        if val == "VIDEO_NOT_FOUND":
            return "VIDEO_NOT_FOUND"

        time.sleep(3)

        play_trigger = self.client.send(
            "Runtime.evaluate",
            {
                "expression": """
                (() => {
                    const video = document.querySelector('video');
                    if (!video) return "VIDEO_ELEMENT_NOT_FOUND";
                    
                    video.play();
                    
                    if (video.paused) {
                        video.muted = true; 
                        video.play();
                        return "PLAYING_MUTED_FALLBACK";
                    }
                    
                    return "PLAYING";
                })()
                """,
                "returnByValue": True
            }
        )

        return f"Navigated to {val} and triggered playback engine."
    
    def subscribe(self):
        """Finds and clicks the subscribe button on the current video page."""
        js_script = """
        (() => {
            const subscribeButton = document.querySelector(
                'ytd-subscribe-button-renderer button, #subscribe-button button'
            );
            
            if (!subscribeButton) return "SUBSCRIBE_BUTTON_NOT_FOUND";
            
            const text = subscribeButton.textContent.toLowerCase();
            if (text.includes("subscribed") || subscribeButton.hasAttribute('subscribed')) {
                return "ALREADY_SUBSCRIBED";
            }
            
            subscribeButton.click();
            return "SUBSCRIBE_CLICKED";
        })()
        """
        return self.client.send(
            "Runtime.evaluate",
            {
                "expression": js_script,
                "returnByValue": True
            }
        )
    
    def comment(self, text: str):
        """Scrolls down, targets the coordinates of the placeholder, types text via hardware keys, and submits."""
        
        # 1. Scroll cleanly to comment section header
        scroll_script = """
        (() => {
            const commentsHeader = document.querySelector('ytd-comments, #comments');
            if (commentsHeader) {
                commentsHeader.scrollIntoView({ block: "start", behavior: "instant" });
                window.scrollBy(0, -100);
                return "SCROLLED_TO_HEADER";
            }
            window.scrollTo(0, 400);
            return "SCROLLED_FALLBACK";
        })()
        """
        self.client.send("Runtime.evaluate", {"expression": scroll_script, "returnByValue": True})
        time.sleep(3)

        # 2. Get precise coordinates of the placeholder box
        coords_script = """
        (() => {
            const box = document.querySelector('#simplebox-placeholder, #simple-box, ytd-comment-simplebox-renderer');
            if (!box) return null;
            
            const rect = box.getBoundingClientRect();
            return {
                x: Math.round(rect.left + rect.width / 2),
                y: Math.round(rect.top + rect.height / 2)
            };
        })()
        """
        coords_res = self.client.send("Runtime.evaluate", {"expression": coords_script, "returnByValue": True})
        coords = coords_res.get("result", {}).get("result", {}).get("value")
        
        if not coords or coords['y'] < 0:
            return "FAILED_COORDINATES_INVALID_OR_OFFSCREEN"
            
        # Ensure window has active context focus
        self.client.send("Runtime.evaluate", {"expression": "window.focus();"})

        # 3. Native hardware mouse press down and up to activate the box
        self.client.send("Input.dispatchMouseEvent", {
            "type": "mousePressed",
            "x": coords["x"],
            "y": coords["y"],
            "button": "left",
            "clickCount": 1
        })
        time.sleep(0.1)
        self.client.send("Input.dispatchMouseEvent", {
            "type": "mouseReleased",
            "x": coords["x"],
            "y": coords["y"],
            "button": "left",
            "clickCount": 1
        })

        # Wait for input text box to fully render and autofocus natively
        time.sleep(2.0)

        # 4. Emulate hardware keyboard typing keystrokes
        for char in text:
            self.client.send("Input.dispatchKeyEvent", {
                "type": "keyDown",
                "text": char,
                "unmodifiedText": char
            })
            self.client.send("Input.dispatchKeyEvent", {
                "type": "keyUp"
            })
            time.sleep(0.02)
            
        time.sleep(1.5)

        # 5. Emulate hardware Ctrl + Enter shortcut sequence to submit comment
        # Control Down
        self.client.send("Input.dispatchKeyEvent", {
            "type": "keyDown",
            "modifiers": 2,
            "windowsVirtualKeyCode": 17,
            "code": "ControlLeft",
            "key": "Control"
        })
        
        # Enter Tap Down/Up
        self.client.send("Input.dispatchKeyEvent", {
            "type": "keyDown",
            "modifiers": 2,
            "text": "\r",
            "unmodifiedText": "\r",
            "windowsVirtualKeyCode": 13,
            "code": "Enter",
            "key": "Enter"
        })
        self.client.send("Input.dispatchKeyEvent", {
            "type": "keyUp",
            "modifiers": 2,
            "windowsVirtualKeyCode": 13,
            "code": "Enter",
            "key": "Enter"
        })
        
        # Control Up
        self.client.send("Input.dispatchKeyEvent", {
            "type": "keyUp",
            "modifiers": 0,
            "windowsVirtualKeyCode": 17,
            "code": "ControlLeft",
            "key": "Control"
        })

        return "COMMENT_SUBMITTED_SUCCESSFULLY"