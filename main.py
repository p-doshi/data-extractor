import pandas as pd
from bs4 import BeautifulSoup
import requests
import os

df = pd.read_excel("black_coffer/Input.xlsx")

output_folder = "output"
os.makedirs(output_folder, exist_ok=True)


def extract_articles(url_link):
    try:
        response = requests.get(url_link)
        content = response.text

        soup = BeautifulSoup(content, "html.parser")
        article_title = soup.find("title").get_text().strip()

        paragraphs = soup.find_all("p")
        article_text = "\n".join(p.get_text() for p in paragraphs)

        return article_title, article_text
    except Exception as e:
        print(f"Error from {url_link} : {e}")
        return None, None


for i, row in df.iterrows():
    url_id = row["URL_ID"]
    url = row["URL"]

    title, art_text = extract_articles(url)

    if title and art_text:
        file_path = os.path.join(output_folder, f"{url_id}.txt")
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(f"{title}\n\n{art_text}")

print("Articles Extracted :)")
