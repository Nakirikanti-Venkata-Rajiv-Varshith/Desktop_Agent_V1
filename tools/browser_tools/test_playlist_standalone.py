import time
import requests
import websocket
import json
import urllib.parse

def run_comprehensive_navigation_test():
    print("[1/2] Connecting to Chromium debug port...")
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
        print("Error: No active YouTube tab detected in Chromium. Please open YouTube first.")
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

    def test_view_panel(name, url):
        print(f"\n---> Moving to Panel View: {name.upper()}")
        send_cdp_eval(f'window.location.href = "{url}";')
        print("Waiting 10 seconds to observe browser layout response...")
        time.sleep(10)

    # 1. Base Core Sidebar Navigation Destinations
    destinations = {
        "Home": "https://www.youtube.com/",
        "Shorts": "https://www.youtube.com/shorts",
        "Subscriptions": "https://www.youtube.com/feed/subscriptions",
        "Your Channel": "https://www.youtube.com/feed/you",
        "History": "https://www.youtube.com/feed/history",
        "Playlists": "https://www.youtube.com/feed/playlists",
        "Watch Later": "https://www.youtube.com/playlist?list=WL",
        "Liked Videos": "https://www.youtube.com/playlist?list=LL",
        "Downloads": "https://www.youtube.com/feed/downloads"
    }

    print("\n[2/2] Starting dynamic panel traversal run...")
    
    # Run structural static layouts
    for panel_name, panel_url in destinations.items():
        test_view_panel(panel_name, panel_url)

    # 2. Dynamic Component Layer Test: Notifications Drawer View
    print("\n---> Triggering Component: NOTIFICATIONS DRAWER")
    # YouTube handles notifications via a top navbar icon drawer element layer
    js_notifications = """
    (() => {
        const notifyBtn = document.querySelector('button[aria-label="Notifications"], ytd-notification-topbar-button-renderer button');
        if (notifyBtn) {
            notifyBtn.click();
            return "SUCCESSFULLY_OPENED_NOTIFICATIONS_TRAY";
        }
        // Fallback direct endpoint if DOM icon clicks are blocked
        window.location.href = "https://www.youtube.com/dashboard?o=U";
        return "FALLBACK_ROUTING_TO_CREATOR_DASHBOARD";
    })()
    """
    print(f"Notification Trigger Status: {send_cdp_eval(js_notifications)}")
    print("Waiting 10 seconds to observe browser view layout...")
    time.sleep(10)

    # 3. Dynamic Component Layer Test: Search Bar Engine Execution
    test_query = "lofi hip hop radio"
    print(f"\n---> Triggering Engine: SEARCH BAR ACTION -> '{test_query}'")
    encoded_query = urllib.parse.quote(test_query)
    search_url = f"https://www.youtube.com/results?search_query={encoded_query}"
    
    send_cdp_eval(f'window.location.href = "{search_url}";')
    print("Waiting 10 seconds to observe search engine results population...")
    time.sleep(10)

    print("\nAll core panels and layout operations traversed successfully. Test pipeline complete!")

if __name__ == "__main__":
    run_comprehensive_navigation_test()