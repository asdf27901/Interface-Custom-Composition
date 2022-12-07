import sys

import requests
from utils import file
from object.env import Env
from object.message import responseAssert
from object.interface import interface as Interface
from alive_progress import alive_bar
from utils.logger import log

try:
    yaml_data = file.get_yaml_data(input('输入接口yaml文件路径:'))
except FileNotFoundError:
    sys.exit('FileNotFoundError: 文件路径错误')

env = Env.parse_obj(yaml_data.pop(0)['env'])
for data in yaml_data:
    interface = Interface.parse_obj(data)
    request_list, filepath = interface.get_all_requests(env)
    length = len(request_list)
    index = 1

    with alive_bar(total=length,
                   force_tty=True,
                   title=interface.interface_name) as bar:

        for request in request_list:
            bar(1)
            info = list(request.keys())[0]
            value = list(request.values())[0]
            print('正在进行第{index}种情况，\033[0;31m{info}\033[0m'.format(index=index, info=info))
            log.debug('正在进行第{index}种情况，{info}'.format(index=index, info=info))
            response = requests.request(**value)
            responseAssert(response=response, filepath=filepath).get_request_message().check_response_message()
            input('按下回车继续')
            index += 1
