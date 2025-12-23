import requests
from bs4 import BeautifulSoup
from langchain_core.tools import tool

def loadwebsite(url: str) -> str:
    html = requests.get(url, timeout=15).text
    soup = BeautifulSoup(html, "html.parser")

    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    
    text = soup.get_text(separator="\n")
    return text