import sys
import argparse
import xml.etree.ElementTree as ET
import pprint
import json

pp = pprint.PrettyPrinter(indent=4)

arg_parser = argparse.ArgumentParser(description='Provide a file to parse')
arg_parser.add_argument('file',
                        metavar='file',
                        type=str,
                        help='A file to parse')
arguments = arg_parser.parse_args()

xml_file = arguments.file
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
                    "drupal_json_generated": False
                }
            }

    def strip_strings_in_dict(obj):
        for key in obj:
            if type(obj[key]) == dict:
                strip_strings_in_dict(obj[key])
             
            if type(obj[key]) == str:
               obj[key] = obj[key].strip()

    strip_strings_in_dict(buffer)    

    articles.append(buffer) 
    # buffer['title']['ru'] = article.find('title_ru').text
    # article.find('title_en').text
    # article.find('authors_list_ru').text

print(json.dumps(articles))
