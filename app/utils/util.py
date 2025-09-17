import json
import os
import sys
from datetime import datetime
from typing import Union, List, Dict, Any
import polars as pl

import ndjson
from utils.logger_wrapper import get_logger

log = get_logger()


def not_implemented(msg):
    raise NotImplementedError(msg)


def error(msg):
    raise Exception(msg)


def find_nodes(node, path_list, wheres):
    if len(path_list) == 0:
        return node
    if isinstance(node, list):
        return [find_nodes(item, path_list, wheres) for item in node]
    if isinstance(node, dict):
        key = path_list[0]
        if key in list(node.keys()):
            del path_list[0]
            return find_nodes(node[key], path_list, wheres)
        else:
            raise Exception


def get_date(date_str, date_format):
    try:
        return datetime.strptime(date_str, date_format)
    except ValueError:
        return None


def read_resource(filename: str, file_dir: str, parquet: bool) -> Union[List[Dict[str, Any]], Dict[str, Any]]:
    """
    Read a fhir resource from file and return the json data
    """
    try:

        if parquet:
            # check if file dir exists
            if not os.path.exists(file_dir):
                log.error(f":sad_but_relieved_face:  Directory {file_dir} does not exist.")
                sys.exit(os.EX_NOINPUT)
            # check if there are parquet files in the directory
            if len([f for f in os.listdir(file_dir) if f.endswith('.parquet')]) == 0:
                log.error(f":sad_but_relieved_face:  No parquet files found in directory {file_dir}.")
                sys.exit(os.EX_NOINPUT)
            # read all parquet files in the directory
            resource_df = pl.read_parquet(os.path.join(file_dir, '*.parquet'))
            log.info(f":thumbs_up:  Resource data in {file_dir} extracted")
            return resource_df.to_dicts()

        else:
            is_bulk = filename.endswith('.ndjson')
            with open(filename, 'r') as file:
                if is_bulk:
                    json_data = ndjson.load(file)
                else:
                    json_data = json.load(file)
                log.info(f":thumbs_up:  Resource data in {filename} extracted")
                return json_data
    except IOError as e:
        log.error(
            f":sad_but_relieved_face:  File {filename} does not exist.")
        log.error(e)
        sys.exit(os.EX_OSFILE)
    except ValueError as e:
        log.error(
            f":sad_but_relieved_face: Cannot parse json data.")
        log.error(e)
        sys.exit(os.EX_OSFILE)


def write_resource_to_file(filename: str, data):
    """
    Write a fhir resource to file
    """
    try:
        # Handle case where filename is empty (when processing parquet from directory)
        if not filename:
            # Generate a default filename based on resource type if available
            if isinstance(data, list) and len(data) > 0 and 'resourceType' in data[0]:
                resource_type = data[0]['resourceType']
                filename = f"{resource_type.lower()}_processed.ndjson"
            else:
                filename = "processed_resources.ndjson"

        is_bulk = filename.endswith('.ndjson')
        filename = filename.replace('.json', '_deid.json') \
            if not is_bulk else filename.replace('.ndjson', '_deid.ndjson')
        # delete file if it exists
        if os.path.exists(filename):
            os.remove(filename)
        log.info(f":writing_hand:  Writing to file {filename}")
        with open(filename, 'w') as resource_file:
            if is_bulk:
                ndjson.dump(data, resource_file)
            else:
                json.dump(data, resource_file, indent=2)
    except IOError as e:
        log.error(
            f":x: could not write to file {filename}.")
        log.error(e)
        sys.exit(1)  # Use standard exit code instead of os.EX_OSFILE

# tokens = ['where', 'first()']
# where_values = { 'position': 'pos'}

# tokens = [ { 'where': { 'key': 'key', 'value': 'value' } }, { 'first()': { 'pos': 0 } }, ]

# def get_wheres(math_str):
#     match_split = math_str.split('.')
#     wheres = []
#     for segment in match_split:
#         print(f'Segment {segment}')
#         for tid, token in enumerate(tokens):
#             print(f'Token {token}')
#             key = list(token.keys())[0]
#             if key in segment:
#                 print(f'Found {token}')
#                 if tid == 0:
#                     where_dict = segment.split(key+'(')[1].split(')')[0].split('=')
#                     print(f'WhereDICT {where_dict}')
#                     if len(where_dict) != 2:
#                         raise Exception
#                     else:
#                         key_str = where_dict[0]
#                         value_str = where_dict[1][1:-1] if ("'" in where_dict[1]) else where_dict[1]
#                         print(f'Key {key_str}\tValue {value_str}')
#                         wheres.append({key_str: value_str})
#                 if tid == 1:
#                     wheres.append(token[key])
#     return wheres

# def get_by_path(resource, el):
#     ret = resource
#     path = el['path'] # "Patient.name"
#     for segment in path.split('.')[1:]:
#         if isinstance(ret, dict):
#             ret = ret.get(segment)
#         elif isinstance(ret, list):
#             for idx, data in enumerate(ret):
#                 if data == el['data']:
#                     ret = ret[idx]
#     return ret
