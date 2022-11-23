# -*- encoding: utf-8 -*-
# Author: Roger·J
# Date: 2022/11/23 14:23
# File: file.py

import yaml


def get_yaml_data(filepath):
    with open(file=filepath, mode='r', encoding='utf8') as f:
        return yaml.safe_load(f)
