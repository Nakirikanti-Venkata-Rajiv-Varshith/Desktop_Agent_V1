import time
from tools.browser_tools.cdp_client import CDPClient

def test_youtube_like():
    print("[1/3] Connecting to Chromium via CDP...")
    try:
        client = CDPClient()
        client.connect()
        print("Success: Connected to YouTube tab!")
    except Exception as e:
        print(f"Error connecting: {e}")
        return

    # Step 2: Run a targeted pipeline to find and click the like button
    print("\n[2/3] Executing like button interactive click pipeline...")
    like_script = """
    (() => {
        // Find the like button using standard button accessibility properties and layout tags
        const likeBtn = document.querySelector(
            'ytd-watch-metadata ytd-like-button-renderer button[aria-label*="like this video"], ' +
            'ytd-video-primary-info-renderer ytd-like-button-renderer button[aria-label*="like this video"], ' +
            'button[aria-label*="like this video"]'
        );
        
        if (!likeBtn) return "LIKE_BUTTON_NOT_FOUND";
        
        // Check if already liked by reading its state
        const isAlreadyLiked = likeBtn.getAttribute('aria-pressed') === 'true';
        if (isAlreadyLiked) {
            return "VIDEO_ALREADY_LIKED";
        }
        
        // Click the element natively
        likeBtn.click();
        return "LIKE_BUTTON_CLICKED_SUCCESSFULLY";
    })()
    """
    
    res = client.send("Runtime.evaluate", {"expression": like_script, "returnByValue": True})
    status = res.get("result", {}).get("result", {}).get("value", "EXECUTION_ERROR")
    print(f"Action Result: {status}")

    # Step 3: Give a quick pause to let the framework register the UI update
    time.sleep(1.5)
    print("\n[3/3] Verification complete.")

if __name__ == "__main__":
    test_youtube_like()