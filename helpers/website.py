import requests
from bs4 import BeautifulSoup

class Website:
    """
    A class to represent a website and its contents.
    """
    def __init__(self, url: str):
        """
        Initialize the Website object with a given URL.
        
        :param url: The URL of the website to scrape
        """
        self.url = url
        self.title, self.text, self.links = self._scrape_website()

    def _scrape_website(self) -> tuple:
        """
        Scrape the website content, extracting title, text, and links.
        
        :return: A tuple containing the title, text content, and links of the website
        """
        response = requests.get(self.url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract title
        title = soup.title.string if soup.title else "No title found"
        
        # Extract text content
        if soup.body:
            for tag in soup.body(["script", "style", "img", "input"]):
                tag.decompose()  # Remove unwanted tags
            text = soup.body.get_text(separator="\n", strip=True)
        else:
            text = ""
        
        # Extract links
        links = [link.get('href') for link in soup.find_all('a') if link.get('href')]
        
        return title, text, links

    def get_contents(self) -> str:
        """
        Get a formatted string of the website contents.
        
        :return: A string containing the website title and text content
        """
        return f"Webpage Title:\n{self.title}\nWebpage Contents:\n{self.text}\n\n"
