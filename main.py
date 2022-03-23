import csv
from pathlib import Path
from utils.library import LibraryAPI
from utils.upload_google_sheet import export_to_google_sheet


def generate_report(out_file="output/output.csv"):
    columns = ["Book_ID", "Book_Title", "Categories", "Authors Names", "Price", "Description"]
    with open(out_file, "w", newline='', encoding='utf-8') as out:
        csv_writer = csv.writer(out)
        csv_writer.writerow(columns)
        library = LibraryAPI()
        library.export_all_books_by_category("relational_databases", csv_writer)
        library.export_all_books_by_category("database_software", csv_writer)
        library.export_all_books_by_category("python", csv_writer)

    return out_file


def main():
    report_file = "output/output.csv"
    try:
        report_file = generate_report()
    except Exception as e:
        print(e)
    if Path(report_file).exists():
        export_to_google_sheet(report_file)


if __name__ == "__main__":
    main()
