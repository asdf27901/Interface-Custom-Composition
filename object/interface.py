# -*- encoding: utf-8 -*-
# Author: Roger·J
# Date: 2022/11/23 12:41
# File: interface.py

import itertools
import os
import object.env as Env
from copy import deepcopy
from pydantic import BaseModel, Field
from typing import Text, Dict, Optional, List, Any
from utils.dict_operate import update_dict, delete_keys_from_dict_by_keys
from utils.logger import log

path = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)

class interface(BaseModel):
    interface_name: Text
    host: Optional[Text]
    url: Optional[Text]
    interface_address: Optional[Text]
    method: Text
    headers: Optional[Dict]
    params: Optional[Dict]
    json_: Optional[Dict] = Field(alias='json')  # 由于BaseModel中存在json属性，所以取名为json_，备注名为json
    data: Optional[Dict]
    files: Optional[Dict]
    optional: Optional[List]
    download: Optional[Dict]

    def __seturl(self) -> None:
        self.url = self.host + self.interface_address
        self.host, self.interface_address = None, None

    def __get_params_correct_data_and_params_error_list(self, params_dict: dict, correct_list: list = None,
                                                        error_list: list = None) -> (list, list):
        """
        字典类型进行传入，根据符号拆分出正确的参数和错误的参数

        :param params_dict: 例如{'pageSize': '10/空值:null', 'pageCurrent': '1/错误:0'}
        :param correct_list: 需要返回的正确参数列表，默认为None
        :param error_list: 需要返回的错误参数列表，默认为None

        :return: correct_list, error_list
        """

        if correct_list is None:
            correct_list = []
        if error_list is None:
            error_list = []

        for key, value in params_dict.items():
            if isinstance(value, dict):
                # 字典类型调用本身方法递归
                self.__get_params_correct_data_and_params_error_list(value, correct_list, error_list)

            elif isinstance(value, list):
                # 遍历列表
                for lis in value:
                    after_split_data = str(lis).split('、')

                    # 错误项中一定包含符号':',使用列表推导式找到所有包含':'的字符串
                    error_data = [x for x in after_split_data if x.__contains__(':')]
                    # 正确项中一定不包含符号':',使用列表推导式找到所有不包含':'的字符串
                    correct_data = [x for x in after_split_data if not x.__contains__(':')]

                    # 将正确项/错误项与对应的key绑定
                    correct_list.append({key: correct_data})
                    error_list.append({key: error_data})

            else:
                after_split_data = str(params_dict[key]).split('、')

                # 错误项中一定包含符号':',使用列表推导式找到所有包含':'的字符串
                error_data = [x for x in after_split_data if x.__contains__(':')]
                # 正确项中一定不包含符号':',使用列表推导式找到所有不包含':'的字符串
                correct_data = [x for x in after_split_data if not x.__contains__(':')]

                # 将正确项/错误项与对应的key绑定
                correct_list.append({key: correct_data})
                error_list.append({key: error_data})

        return correct_list, error_list

    def __get_all_correct_data_and_all_error_list(self) -> [list, list]:
        """
        将自身interface对象转化为字典类型，将yaml文件中params、json、data、files下的参数依次传入，获得params、json、data、files
        中所有正确和错误的参数列表

        :return: [correct, error]
        """
        self.__seturl()
        model = self.dict()
        print('\033[0;31m正在测试{}\033[0m'.format(self.interface_name))
        log.debug('正在测试{}'.format(self.interface_name))
        params_dict = model.get('params', None)
        json_dict = model.get('json_', None)
        data_dict = model.get('data', None)
        file_dict = model.get('files', None)

        correct = []
        error = []
        if params_dict:
            query_add, query_error_dict = self.__get_params_correct_data_and_params_error_list(params_dict)
            correct.extend(query_add)
            error.extend(query_error_dict)

        if json_dict:
            body_add, body_error_dict = self.__get_params_correct_data_and_params_error_list(json_dict)
            correct.extend(body_add)
            error.extend(body_error_dict)

        if data_dict:
            data_add, data_error_dict = self.__get_params_correct_data_and_params_error_list(data_dict)
            correct.extend(data_add)
            error.extend(data_error_dict)

        if file_dict:
            file_add, file_error_dict = self.__get_params_correct_data_and_params_error_list(file_dict)
            correct.extend(file_add)
            error.extend(file_error_dict)

        return correct, error

    def __check_is_no_request_params(self, correct: list, error: list) -> bool:
        """
        将params、json、data、files中所有正确和错误的参数列表传入
        以下两种情况判断为无请求参数
        1、correct、error都为空列表
        2、correct长度为1且correct[0] = {'token': ['None']}

        :param correct: params、json、data、files中所有正确参数列表
        :param error: params、json、data、files中所有错误参数列表
        :return: 满足上述情况返回True，不满足返回False
        """
        if (correct == [] and error == []) or (len(correct) == 1 and correct[0] == {'token': ['None']}):
            return True
        return False

    def __get_correct_requests(self, correct: list, dict_model: dict) -> list:
        """
        传入正确参数列表，将所有可能的正确参数进行笛卡尔积，生成所有可能的正确参数请求列表

        :param correct: params、json、data、files中所有正确参数列表
        :param dict_model: 请求参数模版
        :return: correct_list
        """
        lis = []
        lis_key = []
        zip_list = []
        correct_list = []

        for d in correct:
            for k, v in d.items():
                lis_key.append(k)  # 循环保存key
                lis.append(v)  # 循环保存对应的key所有可能的正确值

        for i in itertools.product(*lis):  # 将lis解包进行笛卡尔积
            zip_list.append(dict(zip(lis_key, i)))  # 将key与生成的笛卡尔积列表通过zip()方法组装，再通过dict()方法转成dict类型

        for i in zip_list:
            model2 = deepcopy(dict_model)  # 深拷贝模版对象，避免后续赋值修改模版对象的值
            update_dict(model2, i)  # 自定义方法去替换嵌套模版对象字典中的value
            correct_list.append(model2)

        return correct_list

    def __check_whether_is_eligible(self, d: dict, condition_dict: dict) -> bool:
        """
        判断是否符合过滤条件

        :param d: 需要判断过滤的字典
        :param condition_dict: 过滤条件
        :return: 需要过滤返回True，不需要过滤返回False
        """
        flag = True

        for key in d:
            if flag and condition_dict.get(key, None) and condition_dict.get(key) != d.get(key):
                flag = False

            if isinstance(d[key], dict):
                flag = self.__check_whether_is_eligible(d[key], condition_dict)

        return flag

    def __filter_optional_parameters(self, correct_list: list, optional_list: list, request_list: list) -> None:
        """
        如果optional参数中包含"｜"符号，则按"｜"进行拆分，如果符合条件则过滤到request_list
        如果optional参数中不包含"｜"符号，则按","进行拆分

        :param correct_list: 笛卡尔积生成的所有可能的正确项请求列表
        :param optional_list: self.optional
        :param request_list: 过滤掉的请求放入到的列表
        :return: None
        """

        for optional in optional_list:
            delete_keys = []

            if optional.__contains__('|'):
                # 根据字典推导式生成可选参数字典
                # tab=1&status=2|businessName  --------> {'tab': '1', 'status': '2'}
                # tab=2&status=3|applyTimeBegin,applyTimeEnd  ----------> {'tab': '2', 'status': '3'}
                condition_dict = {i.split('=')[0]: i.split('=')[1] for i in optional.split('|')[0].split('&')}

                for correct in correct_list:

                    # 判断是否符合过滤条件
                    if self.__check_whether_is_eligible(correct, condition_dict):
                        info = '当' + optional.split('|')[0] + '时' + optional.split('|')[1] + '不传入'
                        # 以正确的请求为模版进行深拷贝
                        correct = deepcopy(correct)

                        for j in optional.split('|')[1].split(','):
                            # 将需要去掉的参数加入到delete_keys列表中
                            delete_keys.append(j)

                        # 根据key删除对应key
                        delete_keys_from_dict_by_keys(correct, delete_keys)
                        # 过滤掉的接口放入到请求列表
                        request_list.append({info: correct})

            else:
                info = optional + '不传入'
                for j in optional.split(','):
                    # 将需要去掉的参数加入到delete_keys列表中
                    delete_keys.append(j)

                # 以正确的请求为模版进行深拷贝
                correct = deepcopy(correct_list[0])
                delete_keys_from_dict_by_keys(correct, delete_keys)
                request_list.append({info: correct})

    def __get_error_requests(self, error_list: list, correct_model: dict, request_list: list) -> None:
        """
        遍历所有错误的参数列表，再遍历参数名下所有错误的值，替换掉正确请求模版中的值，最后放入到请求列表中

        :param error_list: 所有错误的参数列表
        :param correct_model: 正确的参数为模版
        :param request_list: 组合生成的错误参数请求放入到列表
        :return: None
        """

        for d in error_list:
            for k, v in d.items():
                for value in v:
                    info = k + value.split(':')[0]
                    model_dict = deepcopy(correct_model)
                    update_dict(model_dict, {k: value.split(':')[1]})
                    request_list.append({info: model_dict})

    def __set_auth_requests(self, request_list: list, correct: dict, env: Env) -> None:
        """
        为请求中的x-token/token进行赋值

        :param request_list: 请求列表
        :param correct: 正确请求
        :param env: 环境配置对象
        :return: None
        """

        try:
            if self.headers['x-token'] is None:
                x_token = env._Env__backend_login()
                x_token_no_permission = env._Env__backend_login_no_permission()
                for request in request_list:
                    # 对象名._类名__属性/方法 调用私有方法或者私有属性
                    update_dict(request, x_token)

                request_xtoken_invalid = deepcopy(correct)
                update_dict(request_xtoken_invalid, {'x-token': 'xxx'})
                request_xtoken_no_permission = deepcopy(correct)
                update_dict(request_xtoken_no_permission, x_token_no_permission)

                # 新增一个错误请求：x-token无效
                request_list.append({'x-token无效': request_xtoken_invalid})
                # 新增一个错误请求：x-token无权限
                request_list.append({'x-token无权限': request_xtoken_no_permission})

        # 如果找不到x-token这个key，那么使用的就是token
        except KeyError:
            token = env._Env__wx_login()
            for request in request_list:
                update_dict(request, token)
            request_token_invalid = deepcopy(correct)
            update_dict(request_token_invalid, {'token': 'xxx'})
            # 新增一个错误请求：token无效
            request_list.append({'token无效': request_token_invalid})

    def __create_download_file(self) -> str:
        """
        判断是否是下载文件请求

        :return:
        """
        filename = self.download['file_name']
        download_dir = path('../download/')
        filepath = os.path.join(download_dir, filename)

        if not os.path.isdir(download_dir):
            os.mkdir(download_dir)
        self.download = None
        return filepath

    def __delete_all_value_is_none(self, request_list: list) -> None:
        """
        删除请求参数中value为None的key/key为optional
        如果存在json_且value不为None，修改key名为json
        如果存在files且value不为None，根据文件路径获得BufferReader

        :param request_list: 请求列表
        :return: None
        """

        for request in request_list:
            delete_keys = []
            add = {}
            for key, value in list(request.values())[0].items():
                if value is None or key == 'optional':
                    delete_keys.append(key)
                if key == 'json_' and value:
                    delete_keys.append(key)
                    add = {'json': value}
                if key == 'interface_name' and value:
                    delete_keys.append(key)
                if key == 'files' and value:
                    for k, v in value.items():
                        value[k] = open(v, 'rb')

            delete_keys_from_dict_by_keys(request, delete_keys)
            list(request.values())[0].update(add)

    def get_all_requests(self, env: Env) -> [list, Any]:
        """
        生成所有正确的请求和错误请求列表

        :param env: 环境配置对象
        :return: request_list
        """

        request_list = []
        filepath = None
        # 获得params、json、data、files中所有正确和错误的参数列表
        correct, error = self.__get_all_correct_data_and_all_error_list()
        log.debug('正确的参数{}'.format(correct))
        log.debug('错误的参数{}'.format(error))
        if self.download:
            filepath = self.__create_download_file()
        # 所有可能的正确参数进行笛卡尔积，生成所有可能的正确参数请求列表
        correct_list = self.__get_correct_requests(correct, self.dict())
        # 判断是否为无参数请求
        if self.__check_is_no_request_params(correct, error):
            request_list.append({'没有任何参数的请求': self.dict()})
        else:
            for correct in correct_list:
                request_list.append({'所有都传入正确项': correct})
            # 如果self.optional不为空，要进行筛选项过滤
            if self.optional:
                # 过滤可选参数
                self.__filter_optional_parameters(correct_list, self.optional, request_list)
            # 取得所有错误参数请求列表
            self.__get_error_requests(error, correct_list[0], request_list)
        # 为请求中的x-token/token进行赋值
        self.__set_auth_requests(request_list, correct_list[0], env)
        # 删除key为None的key
        self.__delete_all_value_is_none(request_list)

        return request_list, filepath
