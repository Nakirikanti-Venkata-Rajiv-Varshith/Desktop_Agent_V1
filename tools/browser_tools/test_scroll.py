import time
import requests
import websocket
import json
import urllib.parse

def run_scroll_and_play_test():
    print("[1/5] Connecting to Chromium debug port...")
    try:
        tabs = requests.get("http://localhost:9222/json").json()
    except Exception as e:
        print(f"Error: Could not reach port 9222. ({e})")
        return

    target_tab = None
    for tab in tabs:
        if tab.get("type") == "page" and "youtube.com" in tab.get("url", ""):
            target_tab = tab
            break

    if not target_tab:
        print("Error: No active YouTube tab detected. Please open YouTube first.")
        return

    ws = websocket.create_connection(target_tab["webSocketDebuggerUrl"])
    print(f"Connected to tab: {target_tab.get('url')}")

    def send_cdp_eval(script_expression):
        payload = {
            "id": 1,
            "method": "Runtime.evaluate",
            "params": {"expression": script_expression, "returnByValue": True}
        }
        ws.send(json.dumps(payload))
        response = json.loads(ws.recv())
        return response.get("result", {}).get("result", {}).get("value", "ERROR")

    # Step 1: Force search navigation for Justin Bieber
    print("\n[2/5] Searching for 'justin bieber songs'...")
    search_url = f"https://www.youtube.com/results?search_query={urllib.parse.quote('justin bieber songs')}"
    send_cdp_eval(f'window.location.href = "{search_url}";')
    
    print("Waiting 5 seconds for video result layout grid to populate...")
    time.sleep(5)

    # JavaScript engine helper to handle scrolling transitions and click handling dynamically
    js_scroll_and_action = """
    ((targetIndex, action) => {
        const videoCards = Array.from(document.querySelectorAll('ytd-video-renderer, ytd-rich-item-renderer, ytd-compact-video-renderer'));
        
        if (videoCards.length === 0 || targetIndex >= videoCards.length || targetIndex < 0) {
            return "INDEX_OUT_OF_BOUNDS_OR_NO_CARDS";
        }
        
        const card = videoCards[targetIndex];
        
        if (action === "scroll") {
            // Smoothly align the element into the exact center of the screen
            card.scrollIntoView({ behavior: 'smooth', block: 'center' });
            return "SUCCESSFULLY_SCROLLED_TO_ITEM_" + targetIndex;
        } else if (action === "play") {
            // Locate the clickable link or heading anchor within this single specific card frame
            const playLink = card.querySelector('a#video-title, a#thumbnail, a.ytd-video-renderer');
            if (playLink) {
                playLink.click();
                return "PLAY_COMMAND_TRIGGERED_ON_ITEM_" + targetIndex;
            }
            return "COULD_NOT_LOCATE_ANCHOR_ON_CARD";
        }
        return "UNKNOWN_ACTION";
    })
    """

    # Step 2: Scroll DOWN video after video 5 times (Ends on Index 5)
    print("\n[3/5] Starting SCROLL DOWN phase (5 items)...")
    for i in range(1, 6):
        status = send_cdp_eval(f"({js_scroll_and_action})({i}, 'scroll')")
        print(f"Scroll Down Step {i}: {status}")
        time.sleep(3)

    # Play the current video item at index 5
    print("\n---> Launching the 5th video item visible on screen...")
    play_status_1 = send_cdp_eval(f"({js_scroll_and_action})(5, 'play')")
    print(f"Action Status: {play_status_1}")
    
    print("[Waiting] Running video track for 10 seconds...")
    time.sleep(10)

    # Navigate backward back to search context layer mapping index tracking
    print("\n---> Returning to search results viewport...")
    send_cdp_eval("window.history.back();")
    print("Waiting 5 seconds for search results layout to re-initialize...")
    time.sleep(5)

    # Step 3: Scroll UP video after video 3 times from index 5 (5 -> 4 -> 3 -> 2)
    print("\n[4/5] Starting SCROLL UP phase (3 items backward)...")
    target_up_index = 5
    for _ in range(3):
        target_up_index -= 1
        status = send_cdp_eval(f"({js_scroll_and_action})({target_up_index}, 'scroll')")
        print(f"Scroll Up Step to Index {target_up_index}: {status}")
        time.sleep(3)

    # Play the current video item at index 2
    print(f"\n---> Launching the video item at Index {target_up_index} visible on screen...")
    play_status_2 = send_cdp_eval(f"({js_scroll_and_action})({target_up_index}, 'play')")
    print(f"Action Status: {play_status_2}")
    
    print("[Waiting] Running video track for 10 seconds...")
    time.sleep(10)

    print("\n[5/5] Test scrolling and navigation execution pipeline complete!")

if __name__ == "__main__":
    run_scroll_and_play_test()