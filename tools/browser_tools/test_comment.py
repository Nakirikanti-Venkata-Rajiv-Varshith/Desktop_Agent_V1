import time
from tools.browser_tools.cdp_client import CDPClient

def test_youtube_comment():
    print("[1/4] Connecting to Chromium via CDP...")
    try:
        client = CDPClient()
        client.connect()
        print("Success: Connected to YouTube tab!")
    except Exception as e:
        print(f"Error connecting: {e}")
        return

    # Step 2: Scroll perfectly so the placeholder is visible and stationary
    print("\n[2/4] Scrolling precisely to comment section...")
    scroll_script = """
    (() => {
        const commentsHeader = document.querySelector('ytd-comments, #comments');
        if (commentsHeader) {
            // Align to the top of the viewport instead of the center to prevent negative overshoot
            commentsHeader.scrollIntoView({ block: "start", behavior: "instant" });
            // Nudge down slightly so it's fully visible and not under top bars
            window.scrollBy(0, -100);
            return "SCROLLED_TO_HEADER";
        }
        window.scrollTo(0, 400);
        return "SCROLLED_FALLBACK";
    })()
    """
    client.send("Runtime.evaluate", {"expression": scroll_script, "returnByValue": True})
    time.sleep(3)

    # Step 3: Get coordinates and ensure they are absolute/positive
    print("\n[3/4] Finding exact bounding coordinates of the placeholder...")
    coords_script = """
    (() => {
        const box = document.querySelector('#simplebox-placeholder, #simple-box, ytd-comment-simplebox-renderer');
        if (!box) return null;
        
        const rect = box.getBoundingClientRect();
        
        // Safety check: verify if the element is visible in the viewport
        return {
            x: Math.round(rect.left + rect.width / 2),
            y: Math.round(rect.top + rect.height / 2)
        };
    })()
    """
    coords_res = client.send("Runtime.evaluate", {"expression": coords_script, "returnByValue": True})
    coords = coords_res.get("result", {}).get("result", {}).get("value")
    
    if not coords or coords['y'] < 0:
        print(f"❌ FAILED: Coordinates are invalid or off-screen: {coords}")
        return
        
    print(f"Coordinates Found: X={coords['x']}, Y={coords['y']}. Sending hardware Mouse Click...")

    # Focus window first
    client.send("Runtime.evaluate", {"expression": "window.focus();"})

    # Send native mouse press down and up
    client.send("Input.dispatchMouseEvent", {
        "type": "mousePressed",
        "x": coords["x"],
        "y": coords["y"],
        "button": "left",
        "clickCount": 1
    })
    time.sleep(0.1)
    client.send("Input.dispatchMouseEvent", {
        "type": "mouseReleased",
        "x": coords["x"],
        "y": coords["y"],
        "button": "left",
        "clickCount": 1
    })

    # Wait for YouTube to expand the input animation natively
    time.sleep(2.0)

    # Step 4: Emulate hardware keystrokes
    print("\n[4/4] Sending native hardware keystrokes...")
    message = "Great video! Testing automation framework."
    
    for char in message:
        client.send("Input.dispatchKeyEvent", {
            "type": "keyDown",
            "text": char,
            "unmodifiedText": char
        })
        client.send("Input.dispatchKeyEvent", {
            "type": "keyUp"
        })
        time.sleep(0.02)
        
    print("Keystrokes completely dispatched!")
    time.sleep(1.5)

    # Step 5: Press Ctrl + Enter to Post Comment
    print("\n[5/5] Emulating Ctrl + Enter shortcut...")
    
    # Control down
    client.send("Input.dispatchKeyEvent", {
        "type": "keyDown",
        "modifiers": 2,
        "windowsVirtualKeyCode": 17,
        "code": "ControlLeft",
        "key": "Control"
    })
    
    # Enter Down/Up
    client.send("Input.dispatchKeyEvent", {
        "type": "keyDown",
        "modifiers": 2,
        "text": "\r",
        "unmodifiedText": "\r",
        "windowsVirtualKeyCode": 13,
        "code": "Enter",
        "key": "Enter"
    })
    client.send("Input.dispatchKeyEvent", {
        "type": "keyUp",
        "modifiers": 2,
        "windowsVirtualKeyCode": 13,
        "code": "Enter",
        "key": "Enter"
    })
    
    # Control up
    client.send("Input.dispatchKeyEvent", {
        "type": "keyUp",
        "modifiers": 0,
        "windowsVirtualKeyCode": 17,
        "code": "ControlLeft",
        "key": "Control"
    })

    print("Sequence completed.")

if __name__ == "__main__":
    test_youtube_comment()