import sys

import requests
from utils import file
from object.env import Env
from object.message import responseAssert
from object.interface import interface as Interface
from alive_progress import alive_bar

try:
    yaml_data = file.get_yaml_data(input('输入接口yaml文件路径:'))
except FileNotFoundError:
    sys.exit('FileNotFoundError: 文件路径错误')

env = Env.parse_obj(yaml_data.pop(0)['env'])
for data in yaml_data:
    interface = Interface.parse_obj(data)
    request_list = interface.get_all_requests(env)
    length = len(request_list)

    with alive_bar(total=length,
                   force_tty=True,
                   title=interface.interface_name) as bar:

        for request in request_list:
            bar(1)
            info = list(request.keys())[0]
            value = list(request.values())[0]
            response = requests.request(**value)
            responseAssert(response=response).get_request_message().check_response_message()
            input('按下回车继续')
