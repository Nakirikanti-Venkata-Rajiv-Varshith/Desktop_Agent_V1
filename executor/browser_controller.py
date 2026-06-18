import webbrowser
import urllib.parse
from tools.logger import agent_logger

class BrowserController:
    """Handles non-interactive network URL dispatch and searching."""
    
    def open_url(self, url: str) -> bool:
        """Directs the OS browser driver layer to populate target domains directly."""
        if not url:
            return False
        try:
            agent_logger.info(f"Directing browser engine context to: {url}")
            webbrowser.open(url)
            return True
        except Exception as e:
            agent_logger.error(f"Browser interface driver encountered failure: {str(e)}")
            return False

    def search_google(self, query: str) -> bool:
        """Assembles URL search parameters safely to query Google via the browser."""
        if not query:
            return False
        encoded_query = urllib.parse.quote_plus(query)
        target_url = f"https://www.google.com/search?q={encoded_query}"
        return self.open_url(target_url)