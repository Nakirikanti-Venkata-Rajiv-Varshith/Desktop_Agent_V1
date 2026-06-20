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

    def skip_ad(self):
        """Locates the coordinates of the active skip ad button and performs a native hardware click."""
        coords_script = """
        (() => {
            const mainSkipSelectors = [
                '.ytp-skip-ad-button-modern',
                '.ytp-skip-ad-button',
                '.ytp-ad-skip-button-modern',
                '.ytp-ad-skip-button'
            ];
            
            const player = document.querySelector('.html5-video-player');
            if (player && !player.classList.contains('ad-showing')) {
                return "AD_ENDED_NATURALLY";
            }

            for (const selector of mainSkipSelectors) {
                const btn = document.querySelector(selector);
                if (btn) {
                    const style = window.getComputedStyle(btn);
                    if (style.display !== 'none' && style.visibility !== 'hidden' && style.opacity !== '0') {
                        if (btn.offsetHeight > 0 && btn.offsetWidth > 0) {
                            const rect = btn.getBoundingClientRect();
                            return {
                                x: Math.round(rect.left + rect.width / 2),
                                y: Math.round(rect.top + rect.height / 2)
                            };
                        }
                    }
                }
            }
            return "STILL_COUNTING_DOWN";
        })()
        """
        
        max_wait_time = 45
        start_time = time.time()
        coords = None
        
        while (time.time() - start_time) < max_wait_time:
            loop_res = self.client.send("Runtime.evaluate", {"expression": coords_script, "returnByValue": True})
            status = loop_res.get("result", {}).get("result", {}) or {}
            val = status.get("value")
            
            if isinstance(val, dict) and "x" in val:
                coords = val
                break
            elif val == "AD_ENDED_NATURALLY":
                return "AD_CONCLUDED_WITHOUT_CLICK"
                
            time.sleep(1.0)
        else:
            return "SKIP_AD_TIMEOUT"

        # Dispatch native hardware click actions sequence
        self.client.send("Runtime.evaluate", {"expression": "window.focus();"})
        
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

        # Anti-Pause check: Make sure the video keeps moving after the button clears
        time.sleep(0.5)
        force_play_script = """
        (() => {
            const video = document.querySelector('video');
            if (video && video.paused) {
                video.play();
                return "FORCED_PLAYBACK";
            }
            return "ALREADY_PLAYING";
        })()
        """
        self.client.send("Runtime.evaluate", {"expression": force_play_script, "returnByValue": True})
        return "AD_SKIPPED_SUCCESSFULLY"

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
                    const firstVideo = document.querySelector(
                        'ytd-video-renderer a#video-title, ytd-rich-item-renderer a#video-title-link, ytd-grid-video-renderer a#video-title'
                    );
                    if (!firstVideo) return "VIDEO_NOT_FOUND";
                    firstVideo.click();
                    return firstVideo.href;
                })()
                """,
                "returnByValue": True
            }
        )

        val = nav_result.get("result", {}).get("result", {}).get("value", "")
        if val == "VIDEO_NOT_FOUND":
            return "VIDEO_NOT_FOUND"

        return f"Navigated to video link successfully."
    
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
        """Scrolls down, targets the coordinates of the placeholder, types text via hardware keys, submits, waits 1s, and scrolls back up."""
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
            
        self.client.send("Runtime.evaluate", {"expression": "window.focus();"})

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

        time.sleep(2.0)

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

        self.client.send("Input.dispatchKeyEvent", {
            "type": "keyDown",
            "modifiers": 2,
            "windowsVirtualKeyCode": 17,
            "code": "ControlLeft",
            "key": "Control"
        })
        
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
        
        self.client.send("Input.dispatchKeyEvent", {
            "type": "keyUp",
            "modifiers": 0,
            "windowsVirtualKeyCode": 17,
            "code": "ControlLeft",
            "key": "Control"
        })

        time.sleep(1.0)

        scroll_back_script = """
        (() => {
            const videoPlayer = document.querySelector('video, #movie_player');
            if (videoPlayer) {
                videoPlayer.scrollIntoView({ block: "center", behavior: "smooth" });
                return "SCROLLED_BACK_TO_VIDEO";
            }
            window.scrollTo(0, 0);
            return "SCROLLED_BACK_FALLBACK";
        })()
        """
        self.client.send("Runtime.evaluate", {"expression": scroll_back_script, "returnByValue": True})
        time.sleep(1.0)

        return "COMMENT_SUBMITTED_AND_RETURNED_TO_VIDEO"

    def like(self):
        """Finds and clicks the like button to like the current video."""
        js_script = """
        (() => {
            const likeBtn = document.querySelector(
                'ytd-watch-metadata ytd-like-button-renderer button[aria-label*="like this video"], ' +
                'ytd-video-primary-info-renderer ytd-like-button-renderer button[aria-label*="like this video"], ' +
                'button[aria-label*="like this video"]'
            );
            if (!likeBtn) return "LIKE_BUTTON_NOT_FOUND";
            
            if (likeBtn.getAttribute('aria-pressed') === 'true') {
                return "ALREADY_LIKED";
            }
            
            likeBtn.click();
            return "LIKE_BUTTON_CLICKED_SUCCESSFULLY";
        })()
        """
        res = self.client.send("Runtime.evaluate", {"expression": js_script, "returnByValue": True})
        return res.get("result", {}).get("result", {}).get("value", "EXECUTION_ERROR")

    def remove_like(self):
        """Finds the like button and removes the like if it was previously set."""
        js_script = """
        (() => {
            const likeBtn = document.querySelector(
                'ytd-watch-metadata ytd-like-button-renderer button[aria-label*="like this video"], ' +
                'ytd-video-primary-info-renderer ytd-like-button-renderer button[aria-label*="like this video"], ' +
                'button[aria-label*="like this video"]'
            );
            if (!likeBtn) return "LIKE_BUTTON_NOT_FOUND";
            
            if (likeBtn.getAttribute('aria-pressed') === 'false' || !likeBtn.getAttribute('aria-pressed')) {
                return "VIDEO_NOT_LIKED_YET";
            }
            
            likeBtn.click();
            return "LIKE_REMOVED_SUCCESSFULLY";
        })()
        """
        res = self.client.send("Runtime.evaluate", {"expression": js_script, "returnByValue": True})
        return res.get("result", {}).get("result", {}).get("value", "EXECUTION_ERROR")
    
    def skip_forward(self, seconds: int):
        """Jumps the video forward instantly by the specified number of seconds."""
        js_script = f"""
        (() => {{
            const video = document.querySelector('video');
            if (!video) return "VIDEO_ELEMENT_NOT_FOUND";
            
            let targetTime = video.currentTime + {seconds};
            if (targetTime > video.duration) targetTime = video.duration;
            
            video.currentTime = targetTime;
            
            if (video.paused) video.play();
            return "SKIPPED_FORWARD_" + {seconds} + "_SECONDS";
        }})()
        """
        return self.client.send("Runtime.evaluate", {"expression": js_script, "returnByValue": True})

    def skip_backward(self, seconds: int):
        """Jumps the video backward instantly by the specified number of seconds."""
        js_script = f"""
        (() => {{
            const video = document.querySelector('video');
            if (!video) return "VIDEO_ELEMENT_NOT_FOUND";
            
            let targetTime = video.currentTime - {seconds};
            if (targetTime < 0) targetTime = 0;
            
            video.currentTime = targetTime;
            
            if (video.paused) video.play();
            return "SKIPPED_BACKWARD_" + {seconds} + "_SECONDS";
        }})()
        """
        return self.client.send("Runtime.evaluate", {"expression": js_script, "returnByValue": True})