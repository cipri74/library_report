import csv
from library import LibraryAPI


def upload_google_sheets(csv_file):
    pass


def generate_report(out_file="output.csv"):
    columns = ["Book_ID", "Book_Title", "Categories", "Authors Names", "Price", "Description"]
    with open(out_file, "w", newline='') as out:
        csv_writer = csv.writer(out)
        csv_writer.writerow(columns)
        library = LibraryAPI()
        library.export_all_books_by_category("relational_databases", csv_writer)
        library.export_all_books_by_category("database_software", csv_writer)
        library.export_all_books_by_category("python", csv_writer)

    return out_file


def main():
    report_file = generate_report()
    upload_google_sheets(report_file)
    # r = requests.get("https://openlibrary.org/works/OL2035966W.json")
    # print(r.json())


# if __name__ == "__main__":
#     main()

main()