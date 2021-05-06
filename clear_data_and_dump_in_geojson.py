import json
import sys

from loguru import logger

from logging_dir.logging import set_logger, my_exception_hook


def unpack_txt_and_split(fp) -> list:
    with open(fp, 'r') as file:
        file_info = file.read()
    file_info_list = file_info.split('\n')
    return file_info_list


def dump_in_json_file(fp, data) -> None:
    with open(fp, 'w') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def load_geojson_file(fp) -> dict:
    with open(fp, 'r') as file:
        geojson_data = json.load(file)
    return geojson_data


def get_places_names(dict) -> list:
    list_places_names = []
    for elem in dict['features']:
        list_places_names.append(elem['properties'].get('project_name'))
    return list_places_names


def remove_duplicates(list_of_places) -> list:
    list_without_duplicates = []
    number_of_duplicates = 0
    for elem in list_of_places:
        if elem not in list_without_duplicates:
            list_without_duplicates.append(elem)
        else:
            number_of_duplicates += 1
            # logger.debug(elem)

    logger.info(f'Длина изначального списка: {len(list_of_places)}')
    logger.info(f'Количество дублирующихся элементов: {number_of_duplicates}')
    logger.info(f'Длина списка без дубликатов: {len(list_without_duplicates)}')
    return list_without_duplicates


def compare(list_from_table, list_from_geojson) -> int:
    number_of_coincidences = 0
    for elem in list_from_geojson:
        if elem in list_from_table:
            number_of_coincidences += 1
    return number_of_coincidences


def create_geojson_for_elements_from_table_list(parse_data: dict, table_info: list) -> dict:
    dict_for_mesto = {
        "type": "FeatureCollection",
        "features": []
    }
    for elem in parse_data['features']:
        status = elem['properties']['status']
        project_name = elem['properties']['project_name']
        if project_name in table_info and status == 'На голосовании':
            dict_for_mesto["features"].append(elem)
    return dict_for_mesto


JSON_FILE_FROM_TABLE_WITH_LIST_OF_PLACES = 'list_places_from_table.json'
PATH_TO_TXT_FILE_WITH_PLACES = 'places_from_table.txt'
PATH_TO_GEOJSON_FILE_FROM_PARSE = 'reformat_in_geojson_with_status_city_pictures_links.json'
PATH_TO_GEOJSON_FILE_FOR_MESTO = 'final_geojson_file.json'

set_logger()
sys.excepthook = my_exception_hook

list_places_from_table = unpack_txt_and_split(PATH_TO_TXT_FILE_WITH_PLACES)
# dump_in_json_file(JSON_FILE_FROM_TABLE_WITH_LIST, list_places_from_table)
geojson_data_from_parse = load_geojson_file(PATH_TO_GEOJSON_FILE_FROM_PARSE)
# list_places_from_geojson = get_places_names(geojson_data_from_parse)

# logger.debug('Чистим список, полученный парсингом')
# list_places_from_geojson_without_duplicates = remove_duplicates(list_places_from_geojson)
# logger.debug('Чистим список из таблицы')
# list_places_from_table_without_duplicates = remove_duplicates(list_places_from_table)

# number_of_coincidences = compare(list_places_from_table_without_duplicates, list_places_from_geojson_without_duplicates)
# logger.debug(f'Количество совпадений: {number_of_coincidences}')

geojson_data = create_geojson_for_elements_from_table_list(geojson_data_from_parse, list_places_from_table)
dump_in_json_file(PATH_TO_GEOJSON_FILE_FOR_MESTO, geojson_data)