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

                    const video =
                    document.querySelector('video');

                    if (!video)
                        return "NOT_FOUND";

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

                    const video =
                    document.querySelector('video');

                    if (!video)
                        return "NOT_FOUND";

                    video.play();

                    return "PLAYING";

                })()
                """,
                "returnByValue": True
            }
        )
    
    def get_title(self):

        return self.client.execute_js(
            "document.title"
        )


    def search(self, query):

        js = f"""
        (() => {{

            const input =
            document.querySelector(
                'input[name="search_query"]'
            );

            if (!input)
                return "SEARCH_BOX_NOT_FOUND";

            input.focus();

            input.value = "{query}";

            input.dispatchEvent(
                new InputEvent(
                    "input",
                    {{
                        bubbles: true,
                        composed: true
                    }}
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


    # def play_first(self):

    #     return self.client.send(
    #         "Runtime.evaluate",
    #         {
    #             "expression": """
    #             (() => {

    #                 const firstVideo =
    #                 document.querySelector(
    #                     'ytd-video-renderer a#video-title'
    #                 );

    #                 if (!firstVideo)
    #                     return "VIDEO_NOT_FOUND";

    #                 window.location =
    #                 firstVideo.href;

    #                 return firstVideo.href;

    #             })()
    #             """,
    #             "returnByValue": True
    #         }
    #     )

    def play_first(self):

        # Step 1: Find and click/navigate to the first video link
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

        # Extract the value returned by the JS expression
        val = nav_result.get("result", {}).get("result", {}).get("value", "")
        if val == "VIDEO_NOT_FOUND":
            return "VIDEO_NOT_FOUND"

        # Step 2: Wait a moment for the new watch page context to load
        time.sleep(3)

        # Step 3: Re-connect or execute a script on the newly loaded watch page to force play
        # This re-uses your built-in video play logic to bypass Chromium's autoplay restriction
        play_trigger = self.client.send(
            "Runtime.evaluate",
            {
                "expression": """
                (() => {
                    const video = document.querySelector('video');
                    if (!video) return "VIDEO_ELEMENT_NOT_FOUND";
                    
                    // Force playback kickstart
                    video.play();
                    
                    // Double check if browser restriction blocks it, try to unmute/play
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