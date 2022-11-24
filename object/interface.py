# -*- encoding: utf-8 -*-
# Author: Roger·J
# Date: 2022/11/23 12:41
# File: interface.py

from pydantic import BaseModel
from typing import Text, Dict, Optional, List


class interface(BaseModel):
    name: Text
    host: Text
    url: Optional[Text]
    address: Text
    method: Text
    headers: Optional[Dict]
    query: Optional[Dict]
    body: Optional[Dict]
    data: Optional[Dict]
    optional: Optional[List]

    def setUrl(self) -> str:
        return self.host + self.address
