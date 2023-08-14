from pymongo import MongoClient
import json
import requests
from bs4 import BeautifulSoup

from .models import Author, Quote, Tag


def get_mongodb():
    client = MongoClient("mongodb://localhost")

    db = client.hw
    return db


class Scrap:
    def scrape_quotes(self, url):
        base_url_perm = base_url = url

        while True:
            response = requests.get(base_url)
            soup = BeautifulSoup(response.content, "html")

            for quote_div in soup.find_all("div", class_="quote"):
                quote_text = quote_div.find("span", class_="text").get_text()
                author_name = quote_div.find("small", class_="author").get_text()

                # Create or get the Author
                author, created = Author.objects.get_or_create(fullname=author_name)

                # Create the Quote
                quote = Quote.objects.create(quote=quote_text, author=author)

                # Add tags to the Quote
                tags = [tag.get_text() for tag in quote_div.find_all("a", class_="tag")]
                for tag_name in tags:
                    tag, created = Tag.objects.get_or_create(name=tag_name)
                    quote.tags.add(tag)

            next_page = soup.find("li", class_="next")
            if next_page:
                base_url = base_url_perm + next_page.find("a")["href"]
            else:
                break

    def scrape_authors(self, url):
        base_url_perm = base_url = url

        while True:
            response = requests.get(base_url)
            soup = BeautifulSoup(response.text, "lxml")

            for author_div in soup.find_all("div", class_="quote"):
                author_fullname = author_div.find("small", class_="author").get_text()

                # Check if the author already exists in the database
                if not Author.objects.filter(fullname=author_fullname).exists():
                    author_about = (
                        base_url_perm
                        + author_div.find("small", class_="author").find_next("a")[
                            "href"
                        ]
                    )
                    inner_response = requests.get(author_about)
                    inner_soup = BeautifulSoup(inner_response.content, "html.parser")
                    born_date = inner_soup.select("span.author-born-date")
                    born_date_text = "".join([i.text.strip() for i in born_date])
                    born_location = inner_soup.select("span.author-born-location")
                    born_location_text = "".join(
                        [i.text.strip() for i in born_location]
                    )
                    description = inner_soup.select("div.author-description")
                    description_text = "".join([i.text.strip() for i in description])

                    # Create the Author object
                    author = Author.objects.create(
                        fullname=author_fullname,
                        born_date=born_date_text,
                        born_location=born_location_text,
                        description=description_text,
                    )

            next_page = soup.find("li", class_="next")
            if next_page:
                base_url = base_url + next_page.find("a")["href"]
            else:
                break

    def run(self, url):
        self.scrape_authors(url)
        self.scrape_quotes(url)
