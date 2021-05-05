import json
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


set_logger()
sys.excepthook = my_exception_hook
PATH_TO_YAML_FILE = 'result.yml'
PATH_TO_JSON_FILE = 'result.json'
PATH_TO_JSON_BACKUP_FILE = 'result_backup.json'

def unpack_data_from_yaml_file(fp):
    with open(fp, 'r') as file:
        file_info = yaml.load(file, Loader=yaml.FullLoader)
        return file_info


def unpack_data_from_json_file(fp):
    with open(fp, 'r') as file:
        file_info = json.load(file)
        return file_info


def dump_in_json_file(data, fp):
    with open(fp, 'w', encoding='utf8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

end_number = 9000

file_data = unpack_data_from_json_file(PATH_TO_JSON_FILE)
list = file_data

if list:
    list_of_id = []
    # TODO: придумать, что сделать, если файл пустой
    for i in file_data:
        count = i['data'].get('id')
        if count:
            list_of_id.append(count)
    # if not list:
    #     list = []
    # TODO: сделать функцию, которая берет последний элемент списка
    start_number = int(list_of_id[-1]) + 1
else:
    start_number = 0
logger.info(f'Начинаем с номера: {start_number}')

for i in range(start_number, end_number):
    # # TODO: приделать or "Not Found"
    # # TODO: возможно лучше просто последний id забрать из файла
    # print(list_of_id)
    # if i < list_of_id[-1]:
    #     continue
    # if i in list_of_id:
    #     logger.critical('Эта запись уже была собрана')
    #     continue
        # file_data.append(marker_data)
    logger.info(f'Номер записи: {i}')
    marker_data = get_data(i)
    list.append(marker_data)
    dump_in_json_file(list, PATH_TO_JSON_FILE)
    if i % 100 == 0:
        shutil.copy(PATH_TO_JSON_FILE, PATH_TO_JSON_BACKUP_FILE)
        logger.info(f'Сделал бэкап: {PATH_TO_JSON_BACKUP_FILE}')
    # file_info = yaml.dump(file, Loader=yaml.FullLoader)

logger.debug('success, bitch')
