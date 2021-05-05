#!/bin/env python3.9
import json

from argparse import ArgumentParser


def get_json_data(filename: str) -> list:
    with open(filename, "r", encoding="utf-8") as json_file:
        return json.load(json_file)


def parse_features(data: dict):
    return {
        "type": "Feature",
        "properties": {
            "project_name": data.get("name"),
            "description": data.get("description"),
            "region_code": data.get("region").get("code"),
            "region_name": data.get("region").get("name"),
            "vote_counter": data.get("count_votes"),
            "address": data.get("address"),
        },
        "geometry": {
            "type": "Point",
            "coordinates": [
                data.get("map_json").get("features")[0].get("geometry").get("coordinates")[1],
                data.get("map_json").get("features")[0].get("geometry").get("coordinates")[0]
            ]
        }
    }


def evaluate_field(json_data_list: list) -> list:
    features = []
    counter = 0
    for dict_chunk in json_data_list:
        data: dict = dict_chunk.get("data")
        if data:
            if "map_json" in data and data.get("map_json") is not None:
                if len(data.get("map_json").get("features")) > 0:
                    features.append(parse_features(data))
    return {
        "type": "FeatureCollection",
        "features": features
    }


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("-i", "--in", required=True, dest="in_file", type=str,
                        help="specify json file")
    parser.add_argument("-o", "--out", required=True, dest="out_file", type=str,
                        help="specify json file")
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    in_file = args.in_file
    out_file = args.out_file

    json_data_list = get_json_data(in_file)
    geo_data_dict = evaluate_field(json_data_list)

    with open(f"{out_file}.json", "w") as file:
        json.dump(geo_data_dict, file, ensure_ascii=False, indent=4, separators=(',', ': '))
