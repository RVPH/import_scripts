import sys
from os import environ
import argparse
import xml.etree.ElementTree as ET
import json
from pymongo import MongoClient
from transliterate import translit, get_available_language_codes

def strip_strings_in_dict(obj):
    for key in obj:
        if type(obj[key]) == dict:
            strip_strings_in_dict(obj[key])

        if type(obj[key]) == str:
            obj[key] = obj[key].strip()

def convert_xml_to_json(xml_file):

    tree = ET.parse(xml_file)

    root = tree.getroot()

    try:
        year = root.find('year').text
        issue = root.find('issue').text.zfill(2)
        volume = root.find('volume').text
        eissn = root.find('issn').text.replace('-','')
        month = root.find('date').text
    except :
        print('Missing critical fields')
        exit(1)

    articles = []

    for counter, article in enumerate(root.findall('Article'), 1):

        id = '-'.join([eissn, year, issue, str(counter).zfill(2)])
        doi = article.find('doi').text if article.find('doi') != None else None
        title_ru = article.find('title_ru').text if article.find('title_ru') != None else None
        title_en = article.find('title_en').text if article.find('title_en') != None else None
     
        authors_list_ru = [item.text for item in article.find('authors_list_ru') ] if article.find('authors_list_ru') else None
        authors_list_en = [item.text for item in article.find('authors_list_en') ] if article.find('authors_list_en') else None

        authors_info_ru = article.find('authors_info_ru').text if article.find('authors_info_ru') != None else None
        authors_info_en = article.find('authors_info_en').text if article.find('authors_info_en') != None else None

        abstract_ru = article.find('abstract_ru').text if article.find('abstract_ru') != None else None
        abstract_en = article.find('abstract_en').text if article.find('abstract_en') != None else None
         
        rubric = article.find('rubric_ru').text.upper() if article.find('rubric_ru') != None else None

        keywords_ru = [item.text for item in article.find('keywords_ru') ] if article.find('keywords_ru') else None
        keywords_en = [item.text for item in article.find('keywords_en') ] if article.find('keywords_en') else None

        references_ru = [item.text for item in article.find('references_ru') ] if article.find('references_ru') else None
        references_en = [item.text for item in article.find('references_en') ] if article.find('references_en') else None
        
        first_page = article.find('first_page').text if article.find('first_page') != None else None
        last_page = article.find('last_page').text if article.find('last_page') != None else None

        buffer = {"_id" : id,
                  "doi": doi,
                  "journal": {
                        "eISSN": eissn,
                        "volume": int ( volume ),
                        "year": int ( year ),
                        "month": int ( month.split('.')[1] ),
                        "issue": int ( issue )
                   },

                  "title": { "ru": title_ru,
                             "en": title_en 
                     },

                  "authors_list": {
                        "ru": authors_list_ru,
                        "en": authors_list_en
                    },

                  "authors_info": {
                        "ru": authors_info_ru,
                        "en": authors_info_en
                    },

                  "abstract": {
                        "ru": abstract_ru,
                        "en": abstract_en
                    },

                  "rubric": rubric,

                  "keywords": {
                      "ru": keywords_ru,
                      "en": keywords_en
                    },
     
                   "references": {
                       "ru": references_ru,
                       "en": references_en
                    },
                    
                    "pages": {
                        "first": first_page,
                        "last": last_page 
                    },

                    "flags": {
                        "crossref_xml_generated": False,
                    }
                }


        strip_strings_in_dict(buffer)    
        articles.append(buffer) 
    return articles

def export_to_mongo(collection, payload) -> None:
    
    for article in payload:
        collection.replace_one(
            {"_id": article["_id"]}, article, upsert=True)

def fill_english_references(collection):
    collection.update_many({'references.ru.0': 'None'}, {
                           '$set': {'references.ru': None}})
    collection.update_many({'references.en.0': 'None'}, {
                           '$set': {'references.en': None}})
    articles = collection.find({'references.en': None})
    print('Found')
    for article in articles:
        if article['references']['ru']:
            transliterated_list = [translit(
                item, 'ru', reversed=True) for item in article['references']['ru']]
            collection.update_one({'_id': article['_id']}, {
                                  '$set': {'references.en': transliterated_list}})

def fill_english_authors(collection):
    collection.update_many({'authors_list.ru.0': 'None'}, {
                           '$set': {'authors_list.ru': None}})
    collection.update_many({'authors_list.en.0': 'None'}, {
                           '$set': {'authors_list.en': None}})
    articles = collection.find({'authors_list.en': None})
    print('Found')
    for article in articles:
        if article['authors_list']['ru']:
            transliterated_list = [translit(
                item, 'ru', reversed=True) for item in article['authors_list']['ru']]
            collection.update_one({'_id': article['_id']}, {
                                  '$set': {'authors_list.en': transliterated_list}})
   

def main():
    mongo_conection_string = environ['MONGO_DEV_URI']
    client = MongoClient(mongo_conection_string)
    db = client.rvph
    collection = db.articles

    arg_parser = argparse.ArgumentParser(description='Provide a file to parse')
    arg_parser.add_argument('file',
                            metavar='file',
                            type=str,
                            help='A file to parse')
    arguments = arg_parser.parse_args()

    articles_in_json = convert_xml_to_json(arguments.file)
    export_to_mongo(collection, articles_in_json)
    fill_english_references(collection)
    fill_english_authors(collection)

if __name__ == "__main__":
    main()
