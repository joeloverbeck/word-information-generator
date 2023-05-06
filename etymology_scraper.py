import requests
from bs4 import BeautifulSoup


def get_etymology(word):
    url = f"https://www.etymonline.com/word/{word}"
    response = requests.get(url)
    etymology_text = None

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        etymology_section = soup.find("section", {"class": "word__defination--2q7ZH"})

        if etymology_section:
            etymology_text = etymology_section.get_text(strip=True)

    return etymology_text
