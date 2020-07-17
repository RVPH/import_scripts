# Export article data from XLSX-files to MongoDB

from os import listdir, rename, environ
import logging
from pymongo import MongoClient
from openpyxl import load_workbook
from textprocessing_module import id_is_valid


def export_to_mongo() -> None:

    # setup credentials
    mongo_conection_string = environ['MONGO_DEV_URI']

    # setup folders
    incoming_dir = "corrected_xlsx"
    trash_dir = "trash"

    # setup DB connection
    client = MongoClient(mongo_conection_string)
    db = client.rvph
    collection = db.articles

    # setup logging
    logging.basicConfig(filename='app.log',
                        level=logging.INFO,
                        format='%(asctime)s | %(levelname)s | %(message)s',
                        datefmt='%d/%m/%Y %H:%M:%S')

    logstring = "### Export data from XLSX to MongoDB Script started"
    logging.info(logstring)

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

    # Load supplementary journal info (journal title, site etc.)
    # from "journal_info" DB

    journal_info = {}

    for journal in db.journal_info.find({}):
        journal_info[journal["_id"]] = journal

    class article(object):
        def __init__(self) -> None:
            self.id = None
            self.doi = None
            self.title = {}
            self.journal = {}
            self.journal['eISSN'] = None
            self.journal['volume'] = None
            self.journal['issue'] = None
            self.journal['year'] = None
            self.authors_list = {}
            self.authors_info = {}
            self.abstract = {}
            self.keywords = {}
            self.references = {}
            self.pages = {}

    article = article()

    # Actual import

    for file in listdir(incoming_dir):
        if file.endswith(".xlsx"):

            wb = load_workbook(incoming_dir + "/" + file)
            ws = wb.active

            for i, row in enumerate(ws.rows):

                # Collect column titles from Excel file.
                # With this column order is not important

                if i == 0:
                    titles = {}
                    for row_number, title in enumerate(row):
                        titles[title.value] = row_number

                else:

                    if id_is_valid(row[titles[excel_titles['id']]]):

                        # Article info

                        article.id = str(row[titles[excel_titles['id']]].value)
                        article.doi = str(
                            row[titles[excel_titles['doi']]].value)
                        article.rubric = str(
                            row[titles[excel_titles['rubric']]].value)

                        article.title['ru'] = str(
                            row[titles[excel_titles['title_ru']]].value)
                        article.title['en'] = str(
                            row[titles[excel_titles['title_en']]].value)

                        article.abstract['ru'] = str(
                            row[titles[excel_titles['abstract_ru']]].value)
                        article.abstract['en'] = str(
                            row[titles[excel_titles['abstract_en']]].value)

                        article.authors_list['ru'] = str(
                            row[titles[excel_titles['authors_list_ru']]].value).split(', ')
                        article.authors_list['en'] = str(
                            row[titles[excel_titles['authors_list_en']]].value).split(', ')

                        article.authors_info['ru'] = str(
                            row[titles[excel_titles['authors_info_ru']]].value)
                        article.authors_info['en'] = str(
                            row[titles[excel_titles['authors_info_en']]].value)

                        article.keywords['ru'] = str(
                            row[titles[excel_titles['keywords_ru']]].value).split(', ')
                        article.keywords['en'] = str(
                            row[titles[excel_titles['keywords_en']]].value).split(', ')

                        article.references['ru'] = str(
                            row[titles[excel_titles['references_ru']]].value).split('\n')
                        article.references['en'] = str(
                            row[titles[excel_titles['references_en']]].value).split('\n')

                        print(str(row[titles[excel_titles['id']]].value))
                        try:
                            article.pages['first'] = int(
                                str(row[titles[excel_titles['pages']]].value).split(' ')[0])
                        except:
                            article.pages['first'] = None
                        try:
                            article.pages['last'] = int(
                                str(row[titles[excel_titles['pages']]].value).split(' ')[1])
                        except:
                            article.pages['last'] = None

                        # Journal info

                        article.journal['eISSN'] = article.id.split('-')[0]
                        article.journal['volume'] = int(
                            row[titles[excel_titles['volume']]].value)
                        article.journal['year'] = int(article.id.split('-')[1])
                        article.journal['month'] = int(
                            row[titles[excel_titles['month']]].value)
                        article.journal['issue'] = int(
                            article.id.split('-')[2])

                        query = {
                            "_id": article.id,
                            "doi": article.doi,

                            "journal": {
                                "eISSN": article.journal['eISSN'],
                                "volume": article.journal['volume'],
                                "year": article.journal['year'],
                                "month": article.journal['month'],
                                "issue": article.journal['issue']
                            },

                            "title": {
                                "ru": article.title['ru'],
                                "en": article.title['en']
                            },

                            "authors_list": {
                                "ru": article.authors_list['ru'],
                                "en": article.authors_list['en']
                            },

                            "authors_info": {
                                "ru": article.authors_info['ru'],
                                "en": article.authors_info['en']
                            },

                            "abstract": {
                                "ru": article.abstract['ru'],
                                "en": article.abstract['en']
                            },

                            "rubric": article.rubric,

                            "keywords": {
                                "ru": article.keywords['ru'],
                                "en": article.keywords['en']
                            },

                            "references": {
                                "ru": article.references['ru'],
                                "en": article.references['en']
                            },
                            "pages": {
                                "first": article.pages['first'],
                                "last": article.pages['last']
                            },

                            "flags": {
                                "crossref_xml_generated": False,
                                "drupal_json_generated": False
                            }
                        }

                        collection.replace_one(
                            {"_id": article.id}, query, upsert=True)

            # Move parsed file into 'Trash' directory
            rename(incoming_dir + "/" + file, incoming_dir +
                   "/" + trash_dir + "/" + file)

            logstring = file + " has been exported to MongoDB"
            logging.info(logstring)


if __name__ == "__main__":
    export_to_mongo()
