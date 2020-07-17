# Установка

1. Клонировать репозиторий локально:  
`git clone https://github.com/RVPH/import_scripts.git`

2. Переместиться в папку с репозиторием и запустить скрипт установки:  
`cd import_scripts && ./setup.sh`

3. Когда попросят, вставить строку подключения к кластеру Монго (она будет храниться в переменной окружения `MONGO_DEV_URI`). Скрипт создаст виртуальное окружение в папке .venv, установит нужные зависимости и пропишет переменную окружения `MONGO_DEV_URI`в файл .envrc

4. Экспортировать переменные окружения с помощью direnv:  
`direnv allow .`

5. Активировать виртуальное окружение:  
    `source .venv/bin/activate`

6. В папке `samples` лежат файлы-примеры, их можно переместить в папку `incoming_xlsx` для тестов

7. Запустить скрипт по исправлению ошибок:  
    `python3 correct_xlsx.py`

8. Запустить скрипт экспорта данных в Монго:  
    `python3 export_from_XLSX_to_mongo.py`

9. Проверить, что в Монго добавились записи.
