# -*- encoding: utf-8 -*-
# Author: Roger·J
# Date: 2022/11/23 15:03
# File: main.py
import itertools

from utils import file
from typing import Any


def get_optional_num(model: dict) -> int:
    try:
        optional_list = model.pop('optional')
        if optional_list:
            return len(optional_list)
    except KeyError:
        return 0


def get_params_correct_data_and_params_error_list(params_dict: dict, key: Any) -> (dict, dict):

    correct_dict = []
    error_dict = []

    for i in params_dict:
        after_split_data = params_dict[i].split('/')

        error_data = [x for x in after_split_data if x.__contains__(':')]
        correct_data = [x for x in after_split_data if not x.__contains__(':')]

        correct_dict.append({i: [x for x in correct_data]})
        error_dict.append({i: [x for x in error_data]})

    add = {key: correct_dict}
    error_list = {key: error_dict}

    return add, error_list


def get_all_correct_data_and_all_error_list(model: dict):
    query_dict = model.get('query', None)
    body_dict = model.get('body', None)
    data_dict = model.get('data', None)

    add = []
    error_list = []
    if query_dict:
        query_add, query_error_list = get_params_correct_data_and_params_error_list(query_dict, 'query')
        add.append(query_add)
        error_list.append(query_error_list)

    if body_dict:
        body_add, body_error_list = get_params_correct_data_and_params_error_list(body_dict, 'body')
        add.append(body_add)
        error_list.append(body_error_list)

    if data_dict:
        data_add, data_error_list = get_params_correct_data_and_params_error_list(data_dict, 'data')
        add.append(data_add)
        error_list.append(data_error_list)

    for i in add:
        print(i)




yaml_data = file.get_yaml_data('./yaml/interface.yaml')
model_dict = yaml_data[1]

optional_loop_num = get_optional_num(model_dict)

get_all_correct_data_and_all_error_list(model_dict)
