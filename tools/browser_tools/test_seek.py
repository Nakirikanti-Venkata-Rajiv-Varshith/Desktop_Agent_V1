import time
from tools.browser_tools.cdp_client import CDPClient

def test_youtube_seek(seconds: int, direction: str = "forward"):
    """
    Test function to jump forward or backward by an exact number of seconds.
    direction: "forward" or "backward"
    """
    print(f"[1/3] Connecting to Chromium via CDP...")
    try:
        client = CDPClient()
        client.connect()
        print("Success: Connected to YouTube tab!")
    except Exception as e:
        print(f"Error connecting: {e}")
        return

    print(f"\n[2/3] Preparing to skip {seconds}s {direction}...")
    
    # Adjust the operator based on direction
    operator = "+" if direction == "forward" else "-"
    
    seek_script = f"""
    (() => {{
        const video = document.querySelector('video');
        if (!video) return "VIDEO_ELEMENT_NOT_FOUND";
        
        // Calculate the new target time
        let targetTime = video.currentTime {operator} {seconds};
        
        // Safety bounds checks so we don't go below 0 or past the video duration
        if (targetTime < 0) targetTime = 0;
        if (targetTime > video.duration) targetTime = video.duration;
        
        // Apply the new timestamp instantly
        video.currentTime = targetTime;
        
        // Guarantee playback isn't halted during the time seek
        if (video.paused) {{
            video.play();
        }}
        
        return "SUCCESSFULLY_SEEKED_TO_" + Math.round(targetTime) + "_SECONDS";
    }})()
    """

    res = client.send("Runtime.evaluate", {"expression": seek_script, "returnByValue": True})
    status = res.get("result", {}).get("result", {}).get("value", "ERROR")
    print(f"Browser Response: {status}")

    print("\n[3/3] Waiting a brief moment to confirm smooth playback transition...")
    time.sleep(2)
    print("Test execution complete!")

if __name__ == "__main__":
    # Test skipping forward by 30 seconds
    test_youtube_seek(seconds=30, direction="forward")
    
    time.sleep(3)
    
    # Test skipping backward by 10 seconds
    test_youtube_seek(seconds=10, direction="backward")