import csv
import requests


class LibraryAPI:
    URL = "https://openlibrary.org"

    def __init__(self, in_file="input/book_price.csv"):
        self.__in_file = in_file
        self.__book = self.URL + "/works"
        self.__subjects = self.URL + "/subjects"
        self.__author = self.URL + "/authors"
        self.__book_prices = self.load_prices()

    def get_book(self, book_id):
        book_url = f"{self.__book}{book_id}.json"
        response = requests.get(book_url)
        return response.json()

    def get_author(self, author_id):
        author_url = f"{self.__author}{author_id}.json"
        response = requests.get(author_url)
        return response.json()

    def get_url_category_list(self, category, limit=12, offset=0):
        return self.__subjects + f"/{category}.json?limit={limit}&offset={offset}"

    def export_all_books_by_category(self, category, csv_writer, offset=0, chunk=40, max_rows=40):
        url = self.get_url_category_list(category, chunk, offset)
        response = requests.get(url)
        book_details = self.get_books(response.json())
        csv_writer.writerows(book_details)
        nr_rows = len(book_details)
        while len(response.json().get("works")) > 0 and nr_rows < max_rows:
            offset += (chunk+1)
            url = self.get_url_category_list(category, chunk, offset)
            response = requests.get(url)
            book_details = self.get_books(response.json())
            csv_writer.writerows(book_details)
            nr_rows += len(book_details)

    def get_books(self, json_response):
        result = []
        for data in json_response.get("works"):
            book_id = data.get("key", None)
            if book_id is None:
                raise Exception("No book ID found")
            new_book = self.get_book_detail(book_id)
            result.append(new_book)

        return result

    def get_book_detail(self, book_id):
        book_detail = []
        book_url = f"{self.URL}{book_id}.json"
        response = requests.get(book_url)
        raw_id = book_id.split("/")[-1]
        book_detail.append(raw_id)
        book_detail.append(response.json().get("title", "title"))
        book_detail.append(self.get_category(response.json()))
        book_detail.append(self.get_authors(response.json().get("authors")))
        book_detail.append(self.__book_prices.get(raw_id, "price"))
        book_detail.append(self.get_description(response.json()))
        return book_detail

    def get_authors(self, authors_response):
        names = []
        if not isinstance(authors_response, list):
            return "authors"
        for author in authors_response:
            author_id = (author.get("author")).get("key")
            author_url = f"{self.URL}{author_id}.json"
            response = requests.get(author_url)
            names.append(response.json().get("name"))

        return ";".join(names)

    def load_prices(self):
        with open(self.__in_file) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=",")
            result = {}
            for idx, row in enumerate(csv_reader):
                if idx > 0:
                    result[row[0]] = row[1]
            return result

    @staticmethod
    def get_description(response):
        description = response.get("description", None)
        if description is None:
            excerpts = response.get("excerpts", None)
            if excerpts is None:
                return ""
            description = ";".join([(excerpt.get("excerpt")).get("value") for excerpt in excerpts])
        else:
            description = description.get("value", "")
        return description

    @staticmethod
    def get_category(response):
        subjects = response.get("subjects", None)
        if subjects:
            return ";".join([s for s in subjects])
        return "category"

