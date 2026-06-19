from cdp_client import CDPClient

client = CDPClient()

client.connect()

# result = client.send(
#     "Runtime.evaluate",
#     {
#         "expression": """
#         (() => {

#             const input =
#             document.querySelector(
#                 'input[name="search_query"]'
#             );

#             input.focus();

#             input.value = "agentic ai";

#             input.dispatchEvent(
#                 new InputEvent(
#                     "input",
#                     {
#                         bubbles: true,
#                         composed: true
#                     }
#                 )
#             );

#             input.dispatchEvent(
#                 new KeyboardEvent(
#                     "keydown",
#                     {
#                         key: "Enter",
#                         code: "Enter",
#                         keyCode: 13,
#                         which: 13,
#                         bubbles: true
#                     }
#                 )
#             );

#             return true;

#         })()
#         """,
#         "returnByValue": True
#     }
# )

result = client.send(
    "Runtime.evaluate",
    {
        "expression": """
        (() => {

            const video =
            document.querySelector('video');

            if (!video)
                return "NOT_FOUND";

            video.play();

            return {
                paused: video.paused,
                currentTime: video.currentTime
            };

        })()
        """,
        "returnByValue": True
    }
)

print(result)

