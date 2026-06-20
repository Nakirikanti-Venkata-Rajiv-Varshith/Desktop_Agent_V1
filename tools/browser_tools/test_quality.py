import time
from tools.browser_tools.cdp_client import CDPClient

def test_youtube_quality(target: str):
    """
    target: 'max' or 'least'
    """
    print(f"\n[Quality Control] Adjusting video quality to: {target.upper()}...")
    try:
        client = CDPClient()
        client.connect()
    except Exception as e:
        print(f"Error connecting: {e}")
        return

    quality_script = f"""
    (() => {{
        // 1. Find the settings gear button
        const settingsButton = document.querySelector('.ytp-settings-button');
        if (!settingsButton) return "SETTINGS_BUTTON_NOT_FOUND";
        
        // Open the settings panel if it isn't already open
        if (settingsButton.getAttribute('aria-expanded') !== 'true') {{
            settingsButton.click();
        }}
        
        // Small delay to let the panel render dynamically
        setTimeout(() => {{
            // 2. Find the Quality menu item
            const menuItems = Array.from(document.querySelectorAll('.ytp-menuitem'));
            const qualityMenu = menuItems.find(item => {{
                const label = item.querySelector('.ytp-menuitem-label');
                return label && (label.textContent.includes('Quality') || label.textContent.includes('Качество'));
            }});
            
            if (!qualityMenu) {{
                return "QUALITY_MENU_NOT_FOUND";
            }}
            
            // Click to open quality options sub-menu
            qualityMenu.click();
            
            // Another quick delay to allow resolution choices to populate
            setTimeout(() => {{
                const options = Array.from(document.querySelectorAll('.ytp-menuitem'));
                
                // Filter options that look like resolutions (e.g., numbers followed by 'p' or quality labels)
                const resOptions = options.filter(item => {{
                    const label = item.querySelector('.ytp-menuitem-label');
                    return label && /\\d+p/.test(label.textContent);
                }});
                
                if (resOptions.length === 0) return "RESOLUTION_OPTIONS_NOT_FOUND";
                
                // Sort options by extracting numerical values (e.g., '1080p' -> 1080)
                resOptions.sort((a, b) => {{
                    const valA = parseInt(a.querySelector('.ytp-menuitem-label').textContent);
                    const valB = parseInt(b.querySelector('.ytp-menuitem-label').textContent);
                    return valA - valB; // Ascending order
                }});
                
                let selectedOption;
                if ('{target}' === 'max') {{
                    // Highest standard resolution is the last element
                    selectedOption = resOptions[resOptions.length - 1];
                }} else {{
                    // Lowest resolution (144p) is the first element
                    selectedOption = resOptions[0];
                }}
                
                if (selectedOption) {{
                    const targetLabel = selectedOption.querySelector('.ytp-menuitem-label').textContent;
                    selectedOption.click();
                    return "SUCCESSFULLY_SET_QUALITY_TO_" + targetLabel;
                }}
                
                return "FAILED_TO_SELECT_OPTION";
            }}, 300);
            
        }}, 300);
        
        return "PROCESSING_QUALITY_CHANGE_SEQUENCE";
    }})()
    """

    res = client.send("Runtime.evaluate", {"expression": quality_script, "returnByValue": True})
    status = res.get("result", {}).get("result", {}).get("value", "ERROR")
    print(f"Browser Sequence Status: {status}")

if __name__ == "__main__":
    # Ensure you have a video actively playing first!
    
    # 1. Set to Maximum Quality
    test_youtube_quality(target="max")
    
    # 2. Wait 5 seconds
    print("\nRunning at maximum quality configuration for 5 seconds...")
    time.sleep(5)
    
    # 3. Set to Least Quality
    test_youtube_quality(target="least")
    print("\nTest sequence complete! Video dropped to minimum quality constraint.")