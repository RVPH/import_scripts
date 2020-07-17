# Parse all '.xlsx' files in the "incoming_xlsx" directory
# and try to correct them based on set of regular expressions

from os import listdir, path, makedirs, rename, environ
import logging
from openpyxl import load_workbook, Workbook
from textprocessing_module import (process_abstract_field,
                                   process_authors_field,
                                   process_authors_list_field,
                                   process_keywords_field,
                                   process_rubric_field,
                                   process_title_field,
                                   process_references_field,
                                   process_pages_field,
                                   id_is_valid,
                                   volume_is_valid,
                                   month_is_valid)
from transliterate import translit, get_available_language_codes


def correct_xlsx() -> None:

    # setup folders
    incoming_dir = "incoming_xlsx"
    outgoing_dir = "corrected_xlsx"
    trash_dir = "trash"

    # setup logging
    logging.basicConfig(filename='app.log',
                        level=logging.INFO,
                        format='%(asctime)s | %(levelname)s | %(message)s',
                        datefmt='%d/%m/%Y %H:%M:%S')

    logging.info("### XLSX Correction Script started")

    def log_add(file: str, field: str, row: int, cell: 'Excel cell') -> str:
        return ('Incorrect value. File: "' + file + '". ' +
                'Field: "' + field + '". ' +
                'Row: "' + str(row+2) + '". ' +
                'Value: "' + str(cell.value) + '"')


    # dictionary for Excel column titles
    excel_titles = {
        "id": "ID",
        "doi": "DOI",

        "title_ru": "Заголовок статьи",
                    "title_en": "Заголовок статьи (англ.)",

                    "abstract_ru": "Абстракт (краткое содержание)",
                    "abstract_en": "Абстракт (краткое содержание) (англ.)",

                    "keywords_ru": "Ключевые слова",
                    "keywords_en": "Ключевые слова (англ.)",

                    "authors_list_ru": "Список авторов (краткий)",
                    "authors_list_en": "Список авторов (краткий) (англ.)",

                    "authors_info_ru": "Список авторов (полный)",
                    "authors_info_en": "Список авторов (полный) (англ.)",

                    "rubric": "Рубрика",

                    "volume": "Том",
                    "month": "Месяц издания",

                    "references_ru": "Список литературы",
                    "references_en": "Список литературы (англ.)",
                    "pages": "Номера страниц"
    }

    # Scan current directory for ".xlsx" files
    for file in listdir(incoming_dir):
        if file.endswith(".xlsx"):
            logging.info("# Processing a file")

            # load an Excel file into memory
            wb = load_workbook(incoming_dir + "/" + file)

            # set active worksheet
            ws = wb.active

            # Iterate through columns. Column[0].value is the column title.
            # Perform string replacements / value checking based on column title.
            # Text replacement functions stored in textprocessing_module.py

            for i, row in enumerate(ws.rows):

                # Collect column titles from Excel file.
                # With this column order is not important
                if i == 0:
                    titles = {}
                    for col, title in enumerate(row):
                        titles[title.value] = col

                else:

                    if id_is_valid(row[titles[excel_titles['id']]]):
                        logging.info("# Processing a file")
                        process_title_field(
                            row[titles[excel_titles['title_ru']]])
                        process_title_field(
                            row[titles[excel_titles['title_en']]])

                        process_authors_list_field(
                            row[titles[excel_titles['authors_list_ru']]])
                        process_authors_list_field(
                            row[titles[excel_titles['authors_list_en']]])

                        process_authors_field(
                            row[titles[excel_titles['authors_info_ru']]])
                        process_authors_field(
                            row[titles[excel_titles['authors_info_en']]])

                        process_abstract_field(
                            row[titles[excel_titles['abstract_ru']]])
                        process_abstract_field(
                            row[titles[excel_titles['abstract_en']]])

                        process_keywords_field(
                            row[titles[excel_titles['keywords_ru']]])
                        process_keywords_field(
                            row[titles[excel_titles['keywords_en']]])

                        process_rubric_field(
                            row[titles[excel_titles['rubric']]])

                        process_pages_field(row[titles[excel_titles['pages']]])

                        process_references_field(
                            row[titles[excel_titles['references_ru']]])

                        if type(row[titles[excel_titles['references_ru']]].value) is str and not row[titles[excel_titles['references_en']]].value:
                            row[titles[excel_titles['references_en']]].value = translit(row[titles[excel_titles['references_ru']]].value, 'ru', reversed=True)

                        if not id_is_valid(row[titles[excel_titles['id']]]):
                            logging.info(
                                log_add(file, "id", i, row[titles[excel_titles['id']]]))

                        if not volume_is_valid(row[titles[excel_titles['volume']]]):
                            logging.info(
                                log_add(file, "volume", i, row[titles[excel_titles['volume']]]))

                        if not volume_is_valid(row[titles[excel_titles['month']]]):
                            logging.info(log_add(file, "month", i,
                                                 row[titles[excel_titles['month']]]))

            if not path.exists(outgoing_dir):
                makedirs(outgoing_dir)
            wb.save(outgoing_dir + "/" + file)

            if not path.exists(incoming_dir + "/" + trash_dir):
                makedirs(incoming_dir + "/" + trash_dir)

            rename(incoming_dir + "/" + file, incoming_dir +
                   "/" + trash_dir + "/" + file)
            logging.info(file + " has been corrected")


if __name__ == "__main__":
    correct_xlsx()
