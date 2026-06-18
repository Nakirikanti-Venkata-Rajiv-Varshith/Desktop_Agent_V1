import webbrowser
import urllib.parse

class BrowserTool:

    @staticmethod
    def search(query):

        url = (
            "https://www.google.com/search?q="
            + urllib.parse.quote_plus(query)
        )

        webbrowser.open(url)

        return f"Searching for {query}"

    @staticmethod
    def open_url(url):

        webbrowser.open(url)

        return f"Opened {url}"