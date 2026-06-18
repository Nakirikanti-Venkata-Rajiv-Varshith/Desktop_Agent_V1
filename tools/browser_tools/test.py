from tools.browser_tools.browser_focus import focus_chromium
import time

print("Open VSCode and Chromium")
print("Switch to VSCode")

time.sleep(5)

result = focus_chromium()

print("Focus Result:", result)