# -*- encoding: utf-8 -*-
# Author: Roger·J
# Date: 2022/11/23 12:41
# File: interface.py

import itertools
import object.env as Env
from copy import deepcopy
from pydantic import BaseModel, Field
from typing import Text, Dict, Optional, List
from utils.dict_operate import update_dict, delete_keys_from_dict_by_keys


class interface(BaseModel):
    interface_name: Text
    host: Optional[Text]
    url: Optional[Text]
    interface_address: Optional[Text]
    method: Text
    headers: Optional[Dict]
    params: Optional[Dict]
    json_: Optional[Dict] = Field(alias='json')
    data: Optional[Dict]
    files: Optional[Dict]
    optional: Optional[List]

    def __seturl(self) -> None:
        self.url = self.host + self.interface_address
        self.host, self.interface_address = None, None

    def __get_params_correct_data_and_params_error_list(self, params_dict: dict, correct_list: list = None,
                                                        error_list: list = None) -> (list, list):
        if correct_list is None:
            correct_list = []
        if error_list is None:
            error_list = []

        for key, value in params_dict.items():
            if isinstance(value, dict):
                self.__get_params_correct_data_and_params_error_list(value, correct_list, error_list)

            elif isinstance(value, list):
                for lis in value:
                    after_split_data = str(lis).split('/')

                    error_data = [x for x in after_split_data if x.__contains__(':')]
                    correct_data = [x for x in after_split_data if not x.__contains__(':')]

                    correct_list.append({key: [x for x in correct_data]})
                    error_list.append({key: [x for x in error_data]})

            else:
                after_split_data = str(params_dict[key]).split('/')

                error_data = [x for x in after_split_data if x.__contains__(':')]
                correct_data = [x for x in after_split_data if not x.__contains__(':')]

                correct_list.append({key: [x for x in correct_data]})
                error_list.append({key: [x for x in error_data]})

        return correct_list, error_list

    def __get_all_correct_data_and_all_error_list(self) -> [list, list]:
        self.__seturl()
        model = self.dict()
        query_dict = model.get('params', None)
        body_dict = model.get('json_', None)
        data_dict = model.get('data', None)

        correct = []
        error = []
        if query_dict:
            query_add, query_error_dict = self.__get_params_correct_data_and_params_error_list(query_dict)
            correct.extend(query_add)
            error.extend(query_error_dict)

        if body_dict:
            body_add, body_error_dict = self.__get_params_correct_data_and_params_error_list(body_dict)
            correct.extend(body_add)
            error.extend(body_error_dict)

        if data_dict:
            data_add, data_error_dict = self.__get_params_correct_data_and_params_error_list(data_dict)
            correct.extend(data_add)
            error.extend(data_error_dict)

        return correct, error

    def __check_is_no_request_params(self, correct: list, error: list) -> bool:
        if (correct == [] and error == []) or (len(correct) == 1 and correct[0] == {'token': ['None']}):
            return True
        return False

    def __get_correct_requests(self, correct: list, dict_model: dict) -> list:

        lis = []
        lis_key = []
        zip_list = []
        correct_list = []

        for d in correct:
            for k, v in d.items():
                lis.append(v)
                lis_key.append(k)

        for i in itertools.product(*lis):
            zip_list.append(dict(zip(lis_key, i)))

        for i in zip_list:
            model2 = deepcopy(dict_model)
            update_dict(model2, i)
            correct_list.append(model2)

        return correct_list

    def __check_whether_is_eligible(self, d: dict, condition_dict: dict) -> bool:

        flag = True

        for key in d:
            if flag and condition_dict.get(key, None) and condition_dict.get(key) != d.get(key):
                flag = False

            if isinstance(d[key], dict):
                flag = self.__check_whether_is_eligible(d[key], condition_dict)

        return flag

    def __filter_optional_parameters(self, correct_list: list, optional_list: list, request_list: list) -> None:

        for optional in optional_list:
            delete_keys = []

            if optional.__contains__('|'):
                condition_dict = {i.split('=')[0]: i.split('=')[1] for i in optional.split('|')[0].split('&')}

                for correct in correct_list:

                    if self.__check_whether_is_eligible(correct, condition_dict):
                        info = '当' + optional.split('|')[0] + '时' + optional.split('|')[1] + '不传入'
                        correct = deepcopy(correct)

                        for j in optional.split('|')[1].split(','):
                            delete_keys.append(j)

                        delete_keys_from_dict_by_keys(correct, delete_keys)
                        request_list.append({info: correct})

            else:
                info = optional + '不传入'
                for j in optional.split(','):
                    delete_keys.append(j)

                correct = deepcopy(correct_list[0])
                delete_keys_from_dict_by_keys(correct, delete_keys)
                request_list.append({info: correct})

    def __get_error_requests(self, error_list: list, correct_model: dict, request_list: list) -> None:
        for d in error_list:
            for k, v in d.items():
                for value in v:
                    info = k + value.split(':')[0]
                    model_dict = deepcopy(correct_model)
                    update_dict(model_dict, {k: value.split(':')[1]})
                    request_list.append({info: model_dict})

    def __set_auth_requests(self, request_list: list, correct: dict, env: Env) -> None:
        try:
            if self.headers['x-token'] is None:
                for request in request_list:
                    update_dict(request, env._Env__backend_login())

                request_xtoken_invalid = deepcopy(correct)
                update_dict(request_xtoken_invalid, {'x-token': 'xxx'})
                request_xtoken_no_permission = deepcopy(correct)
                update_dict(request_xtoken_no_permission, env._Env__backend_login_no_permission())

                request_list.append({'x-token无效': request_xtoken_invalid})
                request_list.append({'x-token无权限': request_xtoken_no_permission})

        except KeyError:
            for request in request_list:
                update_dict(request, env._Env__wx_login())
            request_token_invalid = deepcopy(correct)
            update_dict(request_token_invalid, {'token': 'xxx'})
            request_list.append({'token无效': request_token_invalid})

    def __delete_all_value_is_none(self, request_list: list) -> None:

        for request in request_list:
            delete_keys = []
            add = {}
            for key, value in list(request.values())[0].items():
                if value is None or key == 'optional':
                    delete_keys.append(key)
                if key == 'json_' and value:
                    delete_keys.append(key)
                    add = {'json': value}
                if key == 'files' and value:
                    for k, v in value.items():
                        value[k] = open(v, 'rb')

            delete_keys_from_dict_by_keys(request, delete_keys)
            request.update(add)

    def get_all_requests(self, env: Env) -> list:
        request_list = []
        correct, error = self.__get_all_correct_data_and_all_error_list()
        correct_list = self.__get_correct_requests(correct, self.dict())
        if self.__check_is_no_request_params(correct, error):
            request_list.append({'没有任何参数的请求': self.dict()})
        else:
            request_list.append({'所有都传入正确项': correct_list[0]})
            if self.optional is not None:
                self.__filter_optional_parameters(correct_list, self.optional, request_list)
            self.__get_error_requests(error, correct_list[0], request_list)
        self.__set_auth_requests(request_list, correct_list[0], env)
        self.__delete_all_value_is_none(request_list)

        return request_list
