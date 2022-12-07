# -*- encoding: utf-8 -*-
# Author: Roger·J
# Date: 2022/12/6 18:19
# File: message.py
import re

from pydantic import BaseModel
from typing import Optional
from requests import Response
from utils.logger import log


class responseAssert(BaseModel):
    response: Response
    filepath: Optional[str]

    class Config:
        arbitrary_types_allowed = True  # 设置BaseModel参数类型为所有类型，False为只适用typing类型

    def download_file(self):
        if self.filepath:
            print("\033[0;32m正在下载{file}\033[0m".format(file=self.filepath))
            log.debug("正在下载{file}".format(file=self.filepath))
            with open(self.filepath, 'wb') as f:
                f.write(self.response.content)
                print("\033[0;32m下载{file}完成\033[0m".format(file=self.filepath))
                log.debug("下载{file}完成".format(file=self.filepath))
        return self

    def check_response_message(self):
        if self.response.status_code != 200:
            print('\033[0;31m状态码都不是200，还测个啥？？？？赶紧打开bilibili学习啦\033[0m')
            print('状态码为:\033[0;31m{code}\033[0m'.format(code=self.response.status_code))
            log.debug('状态码为:{code}'.format(code=self.response.status_code))

        else:
            print('状态码为:\033[0;32m{code}\033[0m'.format(code=self.response.status_code))
            print(
                '响应时间为:{time}'.format(
                    time='\033[0;31m' + str(int(self.response.elapsed.total_seconds() * 1000)) + 'ms\033[0m'
                    if self.response.elapsed.total_seconds() > 0.2
                    else '\033[0;32m' + str(int(self.response.elapsed.total_seconds() * 1000)) + 'ms\033[0m')
            )
            log.debug('状态码为:{code}'.format(code=self.response.status_code))
            log.debug('响应时间为:{time}ms'.format(time=str(int(self.response.elapsed.total_seconds() * 1000))))

            if 'code' in self.response.text or 'Code' in self.response.text:
                print('返回数据:\033[0;32m{data}\033[0m'.format(data=self.response.text))
                log.debug('返回数据:{data}'.format(data=self.response.text))

            else:
                self.download_file()

        return self

    def get_request_message(self):
        print('请求url:{}\n'.format(self.response.url))
        log.debug('请求url:{}'.format(self.response.url))
        print("请求头:{headers}".format(headers=self.response.request.headers))
        log.debug("请求头:{headers}".format(headers=self.response.request.headers))
        try:
            print('请求体:{body}\n'.format(body=self.response.request.body.decode('unicode-escape')))
            log.debug('请求体:{body}'.format(body=self.response.request.body.decode('unicode-escape')))
        except AttributeError:
            print('无请求体\n')
            log.debug('无请求体')

        return self
