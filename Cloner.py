import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

visited = set()

def download_file(url, folder):
    try:
        response = requests.get(url)
        filename = os.path.basename(urlparse(url).path)

        if not filename:
            return

        path = os.path.join(folder, filename)

        with open(path, "wb") as f:
            f.write(response.content)

        print("Downloaded:", filename)

    except:
        print("Failed:", url)


def clone_page(url, folder):
    if url in visited:
        return

    visited.add(url)

    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        if not os.path.exists(folder):
            os.makedirs(folder)

        with open(os.path.join(folder, "index.html"), "w", encoding="utf-8") as f:
            f.write(soup.prettify())

        for tag in soup.find_all(["link", "script", "img"]):

            attr = "href" if tag.name == "link" else "src"

            if tag.get(attr):
                file_url = urljoin(url, tag.get(attr))
                download_file(file_url, folder)

    except:
        print("Error cloning page")


if __name__ == "__main__":
    target = input("Enter website URL: ")
    folder = "cloned_site"

    clone_page(target, folder)

    print("Website cloned successfully.")
