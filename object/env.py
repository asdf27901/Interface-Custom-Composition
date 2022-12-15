# -*- encoding: utf-8 -*-
# Author: Roger·J
# Date: 2022/11/23 13:43
# File: env.py
import os
import sys

import diskcache
import requests
from pydantic import BaseModel
from typing import Text
from diskcache import Cache
from utils.logger import log

path = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)


class Env(BaseModel):
    wx_app_host: Text
    backend_host: Text
    wx_code: Text
    username: Text
    password: Text
    username_no_permissions: Text
    password_no_permissions: Text
    cache: diskcache.Cache = Cache('./cache/user_cache')

    class Config:
        arbitrary_types_allowed = True  # 设置BaseModel参数类型为所有类型，False为只适用typing类型

    def __wx_login(self) -> dict:
        """
        先从文件缓存中获取小程序token
        如果缓存中存在，去判断token是否失效，不失效则返回token，失效则终止程序
        如果缓存中不存在，调用微信静默登陆接口，将token先存入文件缓存中，再将token以字典形式返回

        :return: 返回字典类型小程序token
        """

        token = self.cache.get('token', default=False)
        if token:
            response = requests.post(url=self.wx_app_host + '/xct/message/countMessage',
                                     json={
                                         'token': token
                                     },
                                     headers={'Content-Type': 'application/json;charset=UTF-8'})
            if response.status_code != 200:
                raise Exception("小程序服务正在重启，请稍后再试")
            if response.text.__contains__('Token 失效'):
                print("Token已经失效，请重新获取小程序code")
                os.remove(path('../cache/user_cache/cache.db'))
                sys.exit(1)

            print('缓存中拿到的token:\033[0;31m{token}\033[0m'.format(token=token))
            log.debug('缓存中拿到的token:{token}'.format(token=token))
            return {'token': token}

        else:
            __login_wxapp_response = requests.post(url=self.wx_app_host + '/xct/auth/customerLoginByWeixin',
                                                   json={
                                                       'data':
                                                           {'code': self.wx_code}
                                                   },
                                                   headers={'Content-Type': 'application/json;charset=UTF-8'})

            if __login_wxapp_response.status_code != 200:
                raise Exception("小程序服务正在重启，无法拿到token")
            try:
                token = __login_wxapp_response.json()['data']['token']
                self.cache.set('token', token)
                print('微信重新登陆获取到的token:\033[0;31m{token}\033[0m'.format(token=token))
                log.debug('微信重新登录获取到的token:{token}'.format(token=token))
                return {'token': token}
            except KeyError:
                print("小程序code失效请重新输入")
                sys.exit(1)

    def __backend_login(self) -> dict:
        """
        先从文件缓存中获取后台x-token
        如果缓存中存在，直接将x-token以字典形式返回
        如果缓存中不存在，调用后台登陆接口，将x-token先存入文件缓存中，再将x-token以字典形式返回

        :return: 返回字典类型后台x-token
        """

        x_token = self.cache.get('x-token', default=False)
        if x_token:
            log.debug('缓存中拿到的x-token:{x_token}'.format(x_token=x_token))
            return {'x-token': x_token}
        else:
            __login_backend_response = requests.post(url=self.backend_host + '/user/login',
                                                     json={
                                                         'username': self.username,
                                                         'password': self.password
                                                     },
                                                     headers={'Content-Type': 'application/json;charset=UTF-8'})

            if __login_backend_response.status_code != 200:
                raise Exception("后台服务正在重启，无法拿到token")
            try:
                x_token = __login_backend_response.json()['data']['token']
                self.cache.set('x-token', x_token)
                log.debug('重新登录获取到的x-token:{x_token}'.format(x_token=x_token))
                return {'x-token': x_token}
            except TypeError:
                print("后台用户名密码有误，请修改配置文件")
                sys.exit(1)

    def __backend_login_no_permission(self) -> dict:
        """
        先从文件缓存中获取后台无权限x-token-no-permissions
        如果缓存中存在，直接将x-token以字典形式返回
        如果缓存中不存在，调用后台登陆接口，将x-token先存入文件缓存中，再将x-token以字典形式返回

        :return: 返回字典类型后台x-token
        """

        x_token_no_permission = self.cache.get('x-token-no-permissions', default=False)
        if x_token_no_permission:
            log.debug('缓存中拿到的x_token_no_permission:{x_token_no_permission}'.format(
                x_token_no_permission=x_token_no_permission))
            return {'x-token': x_token_no_permission}
        else:
            __login_backend_response = requests.post(url=self.backend_host + '/user/login',
                                                     json={
                                                         'username': self.username_no_permissions,
                                                         'password': self.password_no_permissions
                                                     },
                                                     headers={'Content-Type': 'application/json;charset=UTF-8'})

            if __login_backend_response.status_code != 200:
                raise Exception("后台服务正在重启，无法拿到token")
            try:
                x_token_no_permission = __login_backend_response.json()['data']['token']
                self.cache.set('x-token-no-permissions', x_token_no_permission)
                log.debug('重新登录获取到的x_token_no_permission:{x_token_no_permission}'.format(
                    x_token_no_permission=x_token_no_permission))
                return {'x-token': x_token_no_permission}
            except TypeError:
                print("后台用户名密码有误，请修改配置文件")
                sys.exit(1)
