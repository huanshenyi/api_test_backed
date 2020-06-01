__author__ = "ハリネズミ"
import requests
from urllib import parse
import json
import re


def request(api):
    """
    :param api: apiデータのオブジェクト
    :return:
    host: http://www.baidu.com
    method: /q?wd=python
    path: //www.xx.com/q?wd=python
    """
    host = api.host.host
    method = api.http_method
    path = api.path
    url = parse.urljoin(host, path)
    data = {}
    if api.data:
        data_list = json.loads(api.data, encoding="utf-8")
        for data_dict in data_list:
            # [{name: "username", value:"zhiliao"}]
            data[data_dict["name"]] = data_dict["value"]
    headers = {}
    if api.headers:
        header_list = json.loads(api.headers, encoding="ut-8")
        for header_dict in header_list:
            headers[header_dict["name"]] = header_dict["value"]
    resp = requests.request(method, url, headers=headers, data=data)
    return resp

