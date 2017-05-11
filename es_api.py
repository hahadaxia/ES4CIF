# -*- coding: utf-8 -*-
from elasticsearch import Elasticsearch
from logger import logger
from es_ip_port import ES_IP_PORT
import re
from query_api import select_observable,select_observable_gte25
select_ip = {
  "query": {
    "term": {
      "observable": ""
    }
  }
}

select_ip_gte25 = {
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


class ESConnection(object):
    def __init__(self, host, port):
        """
        与es建立链接
        :param host: es主机地址
        :param port: es端口号
        """
        try:
            self.conn = Elasticsearch([{'host': host, 'port': port}])
        except Exception as e:
            logger.error('Elastic Search %s connect error:%s' % (host, e))
            raise Exception(e)

    def search(self, index=None, doc_type=None, body=None):
        """
        根据查询结构查找es中index目录下的数据
        :param index: 待查询的目录,支持模糊匹配
        :param doc_type: 待查询文件的类型
        :param body: 待查询结构 'query'
        :return: 以json格式返回查询结果
        """
        try:
            result = self.conn.search(index=index, doc_type=doc_type, body=body, scroll='1m', timeout='10s')
            logger.info('es search hit %d items' % (result['hits']['total']))
            return result
        except Exception as e:
            logger.error('es search error: %s' % e)
            # raise Exception(e)

    def count(self, index=None, doc_type=None, body=None):
        """
        返回查询结果的数量
        :param index: index名
        :param doc_type: 文件类型
        :param body: 查询结构
        :return: 返回命中次数
        """
        try:
            result = self.conn.count(index=index, doc_type=doc_type,body=body)
            logger.info('es count: %s' % result)
            return result['count']
        except Exception as e:
            logger.error('es count error: %s' % e)
            raise Exception(e)

    def create(self, index, doc_type, id, body):
        """
        在es中写入数据
        :param index: 待写入数据的index
        :param doc_type: 待写入数据的文件类型
        :param id: 数据的id(唯一)
        :param body: 待写入数据（json格式）
        :return: 返回创建是否成功的信息
        """
        try:
            result = self.conn.create(index=index, doc_type=doc_type, id=id, body=body, refresh='true', timeout='60s')
            return result
        except Exception as e:
            logger.error('es create error: %s' %e)
            raise Exception(e)

    def createindex(self, index):
        """
        创建一个index
        :param index: index名
        :return: 返回创建是否成功的信息
        """
        try:
            result = self.conn.indices.create(index=index)
            return result
        except Exception as e:
            logger.error('es create error: %s' % e)
            raise Exception(e)

    def createmapping(self, index, mapping_body):
        """
        在index目录下创建数据mapping
        :param index: index名
        :param mapping_body: json格式的 mapping
        :return: 返回创建是否成功的结果
        """
        try:
            result = self.conn.indices.create(index=index,body=mapping_body)
            return result
        except Exception as e:
            logger.error('es create error: %s' % e)
            raise Exception(e)

    def deleteindex(self, index):
        """
        删除es中某个index
        :param index: index名
        :return: 返回删除是否成功的信息
        """
        try:
            result = self.conn.indices.delete(index=index, ignore=[400, 404])
            return result
        except Exception as e:
            logger.error('es delete error: %s' % e)
            raise Exception(e)

    def ip_hits(self, source_file_name, output_file_name, query_body):
        """
        函数用来统计文件中ip在开源数据中命中次数
        :param source_file_name: 需要统计ip命中数的源文件
        :param output_file_name: 命中次数输出文件
        :param query_body: 查询结构
        :return:
        """
        es_ip_port = ES_IP_PORT()
        index = "cif.observables*"
        es = ESConnection(es_ip_port.getIp(), es_ip_port.getPort())
        regex = '.*?((?:\d{1,3}\.){3}(?:\d{1,3})).*'
        pattern = re.compile(regex)
        try:
            infile = open(source_file_name, 'r')
            try:
                outfile = open(output_file_name, 'w')
                for line in infile:
                    match = pattern.match(line)
                    if match:
                        dst_ip = match.group(1)
                        if query_body == select_observable:
                            query_body["query"]["term"]["observable"] = dst_ip
                        elif query_body == select_observable_gte25:
                            query_body["query"]["bool"]["must"][0]["match"]["observable"] = dst_ip
                        else:
                            print "no such query body\n"
                            raise Exception(e)
                        result = es.search(index, query_body)
                        count = result['hits']['total']
                        if count != 0:
                            try:
                                source_example = result['hits']['hits'][0]["_source"]
                            except KeyError as e:
                                print ("KeyError:" + str(e))
                            try:
                                tags = str(source_example["tags"])
                            except KeyError as e:
                                print ("KeyError:" + str(e))
                                tags = '[]'
                            try:
                                provider = str(source_example["provider"])
                            except KeyError as e:
                                provider = "none"
                            confidence = str(source_example["confidence"])
                            outfile.writelines('observable:' + dst_ip
                                               + ',count:' + str(count)
                                               + ',provider:' + provider
                                               + ',tags:' + tags
                                               + ',confidence:' + confidence + '\n')
                    else:
                        pass
            except IOError as err:
                print ('File Error:' + str(err))
            finally:
                outfile.close()
        except IOError as err:
            print ('File Error:' + str(err))
        finally:
            infile.close()




"""
es = ESConnection('127.0.0.1','9200')
    dst_ip_file_name = "DstIP.txt"
    dst_hits_output_info_name = "output.txt"
    es.ip_hits(dst_ip_file_name, dst_hits_output_info_name, select_ip_gte25)
def std_output(infile, outfile, query_body):
    start_time = datetime.datetime.now()
    count_ip_hits(infile, outfile, query_body)
    finish_time = datetime.datetime.now()
    spend_time = finish_time - start_time
    print "-------------time used : %s ------------------\n" % str(spend_time)
    print "-------------this is the end------------------\n"
"""






