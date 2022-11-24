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


def get_params_correct_data_and_params_error_list(params_dict: dict) -> (dict, dict):

    correct_dict = []
    error_dict = []

    for i in params_dict:
        after_split_data = params_dict[i].split('/')

        error_data = [x for x in after_split_data if x.__contains__(':')]
        correct_data = [x for x in after_split_data if not x.__contains__(':')]

        correct_dict.append({i: [x for x in correct_data]})
        error_dict.append({i: [x for x in error_data]})

    return correct_dict, error_dict


def get_all_correct_data_and_all_error_list(model: dict):
    query_dict = model.get('query', None)
    body_dict = model.get('body', None)
    data_dict = model.get('data', None)
    # query_add, query_error_list, body_add, body_error_list, data_add, data_error_list = [], [], [], [], [], []

    add = []
    error_list = []
    if query_dict:
        query_add, query_error_dict = get_params_correct_data_and_params_error_list(query_dict)
        add.extend(query_add)
        error_list.extend(query_error_dict)

    if body_dict:
        body_add, body_error_dict = get_params_correct_data_and_params_error_list(body_dict)
        add.extend(body_add)
        error_list.extend(body_error_dict)

    if data_dict:
        data_add, data_error_dict = get_params_correct_data_and_params_error_list(data_dict)
        add.extend(data_add)
        error_list.extend(data_error_dict)

    return add, error_list


def get_error_requests(error_list: dict, model: dict, correct_data: dict) -> list:
    request_list = []

    for d in error_list:
        for k, v in d.items():
            for i in v:
                model.update(correct_data)
                info = k + i.split(':')[0]
                model[k] = i.split(':')[1]
                requests_list.append({info: deepcopy(model)})

    return request_list


def get_all_correct_combination(correct: list) -> list:

    lis = []
    lis_key = []
    correct_list = []

    for d in correct:
        for k, v in d.items():
            lis.append(v)
            lis_key.append(k)

    for i in itertools.product(*lis):
        correct_list.append(dict(zip(lis_key, i)))

    print(correct_list)

    return correct_list

def get_correct_requests(correct: dict) -> list:
    # TODO 从model_dist中获取query参数、body参数、data参数，然后再从所有正确结果中抽取出来
    pass



yaml_data = file.get_yaml_data('./yaml/interface.yaml')
model_dict = yaml_data[1]
print(model_dict)

optional_loop_num = get_optional_num(model_dict)

correct, error = get_all_correct_data_and_all_error_list(model_dict)

get_all_correct_combination(correct)
