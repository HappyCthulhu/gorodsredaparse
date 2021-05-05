import json
import os
import shutil
import sys

import requests
import yaml
from loguru import logger

from logging_dir.logging import set_logger, my_exception_hook


def get_data(number):
    url = f"https://pos.gosuslugi.ru/og/api/v1/improvement/{number}"
    logger.debug(f'Ссылка: https://admin.za.gorodsreda.ru/web-widget/#web-widget/post/{number}')

    payload = {}
    headers = {
        'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
        'Accept': 'application/json, text/plain, */*',
        'DNT': '1',
        'Authorization': 'Bearer hPCQ2E5hAivHY76lE6yyrd9toiLhN_rm_1618577471',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
        'Sec-Fetch-Site': 'cross-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Cookie': '_csrf=xDMZ5PkBcYuiJhrHlyiByyAycUgfAyFc'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    label_data = json.loads(response.text)
    logger.debug(f'Название объекта: {label_data["data"]["name"]}')
    # list.append(response.text)
    return label_data
    # print(response.text)


def unpack_data_from_yaml_file(fp):
    with open(fp, 'r') as file:
        file_info = yaml.load(file, Loader=yaml.FullLoader)
        return file_info


def unpack_data_from_json_file(fp):
    with open(fp, 'r', encoding='utf-8') as file:
        file_info = json.load(file)
        return file_info


def dump_in_json_file(data, fp):
    with open(fp, 'w', encoding='utf8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
        
def check_json_file_exist(fp):
    if not os.path.isfile(fp):
        with open(fp, 'w', encoding='utf-8') as file:
            empty_list = []
            json.dump(empty_list, file) 


set_logger()
sys.excepthook = my_exception_hook
PATH_TO_YAML_FILE = 'result.yml'
PATH_TO_JSON_FILE = 'result.json'
PATH_TO_JSON_BACKUP_FILE = 'result_backup.json'
END_COUNT = 9000

check_json_file_exist(PATH_TO_JSON_FILE)
file_data = unpack_data_from_json_file(PATH_TO_JSON_FILE)
list = file_data
START_COUNT = 0

if list:
    list_of_id = []
    for i in file_data:
        count = i['data'].get('id')
        if count:
            list_of_id.append(count)
    START_COUNT = int(list_of_id[-1]) + 1

logger.info(f'Начинаем с номера: {START_COUNT}')

for i in range(START_COUNT, END_COUNT):
    logger.info(f'Номер записи: {i}')
    marker_data = get_data(i)
    list.append(marker_data)
    dump_in_json_file(list, PATH_TO_JSON_FILE)
    if i % 100 == 0:
        shutil.copy(PATH_TO_JSON_FILE, PATH_TO_JSON_BACKUP_FILE)
        logger.info(f'Сделал бэкап: {PATH_TO_JSON_BACKUP_FILE}')

logger.debug('success, bitch')
