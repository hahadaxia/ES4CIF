# -*- coding: utf-8 -*-
select_observable = {
  "query": {
    "term": {
      "observable": ""
    }
  }
}

select_observable_gte25 = {  # 可信度不小于25, tags不包含'search'
  "query": {
      "bool": {
            "must": [
                {"match": {"observable": "0.0.0.0"}},
                {"range": {"confidence": {"gte": 25}}}
            ],
            "must_not": {"match": {"tags": "search"}}

        }
    }
}

# 你好

print "你好"