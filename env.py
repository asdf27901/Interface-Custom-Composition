# -*- encoding: utf-8 -*-
# Author: Roger·J
# Date: 2022/11/23 13:43
# File: env.py

import sys

import diskcache
import requests
from pydantic import BaseModel
from typing import Text
from diskcache import Cache


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
        arbitrary_types_allowed = True

    def wx_login(self) -> str:
        token = self.cache.get('token', default=False)
        if token:
            return token
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
                self.cache.set('token', __login_wxapp_response.json()['data']['token'])
            except KeyError:
                print("小程序code失效请重新输入")
                sys.exit(1)

    def backend_login(self) -> str:
        x_token = self.cache.get('x-token', default=False)
        if x_token:
            return x_token
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
                self.cache.set('x-token', __login_backend_response.json()['data']['token'])
            except TypeError:
                print("后台用户名密码有误，请修改配置文件")
                sys.exit(1)

    def backend_login_no_permission(self):
        x_token_no_permission = self.cache.get('x-token-no-permissions', default=False)
        if x_token_no_permission:
            return x_token_no_permission
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
                self.cache.set('x-token-no-permissions', __login_backend_response.json()['data']['token'])
            except TypeError:
                print("后台用户名密码有误，请修改配置文件")
                sys.exit(1)

    def del_cache(self):
        self.cache.expire()
