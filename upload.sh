#!/bin/bash
set -e
python3 correct_xlsx.py
python3 export_from_XLSX_to_mongo.py
exit 0
