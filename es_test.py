# -*- coding: utf-8 -*-
from es_api import ESConnection
import time


def test_es():
    es = ESConnection('172.16.100.169', '9200')
    index = 'test_index'
    doc_type = 'test_doc'
    time1 = str(time.time())
    time2 = time1[:10] + '000'
    timestamp = time2
    id = timestamp  # 以时间创建ID，避免id不唯一
    test_mapping = {
        "mappings": {
            "test_doc":{
                "_all":{"enabled": "false"},
                "properties":{
                    "timestamp":{"type":"date"},
                    "observable": {"type":"keyword"},
                    "openti": {"type":"nested"},
                    "threatbook": {"type":"nested"},
                    "virustotal": {"type":"nested"},
                    "shodan":{"type":"nested"}
                }
            }
        }
    }
    # es.deleteindex(index)   # 删除index
    # es.createmapping(index, test_mapping)   # 创建mapping，注意mapping一经创建无法修改，只能通过删除index再重新创建
    null = None
    test_body = {
        "observable":"8.8.8.8",
        "timestamp": timestamp,
        "shodan": {
            "portlist": [" 80/Tor built-in httpd"],
            "location": {
                "city": null,
                "region_code": null,
                "area_code": null,
                "longitude": 2.3386999999999887,
                "country_code3": "FRA",
                "latitude": 48.85820000000001,
                "postal_code": null,
                "dma_code": null,
                "country_code": "FR",
                "country_name": "France"
            }
        },
        "openti": {
            "confidence": 65,
            "provider": "botscout.com",
            "tags": ["botnet"]
        },
        "virustotal": {
            "ip": "80.67.172.162",
            "ldu": {
                "count": "1/68",
                "url": "http://kvlj.www1.biz/",
                "time": "2016-11-01 16:11:08"
            },
            "pdns": {
                "domain": "antvirus.ddns.com.br",
                "time": "2017-02-03"
            }
        },
        "threatbook": {
            "now": {
                "data": ["Zombie", "IDC"]
            },
            "expired": {}
        }
    }
    es.create(index, doc_type, id, test_body)  # 创建数据
    test_query = {
            "query": {
                "term": {
                    "observable": "8.8.8.8"
                }
            }
    }
    info = es.search(index, doc_type, test_query)  # 查询数据
    print info

if __name__ == "__main__":
    test_es()
