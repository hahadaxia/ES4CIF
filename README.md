# ElasticSearch API
### class ESConnection
* __init__:
> __init__(self, host, port):
        与es建立链接
        :param host: es主机地址
        :param port: es端口号      
* search:
> search(self, index=None, doc_type=None, body=None):
        根据查询结构查找es中index目录下的数据
        :param index: 待查询的目录,支持模糊匹配
        :param doc_type: 待查询文件的类型
        :param body: 待查询结构 'query'
        :return: 以json格式返回查询结果
* count:
> count(self, index=None, doc_type=None, body=None):
        返回查询结果的数量
        :param index: index名
        :param doc_type: 文件类型
        :param body: 查询结构
        :return: 返回命中次数
* create
> create(self, index, doc_type, id, body):
        在es中写入数据
        :param index: 待写入数据的index
        :param doc_type: 待写入数据的文件类型
        :param id: 数据的id（唯一）
        :param body: 待写入数据（json格式）
        :return: 返回创建是否成功的信息
* createindex
>createindex(self, index):
        创建一个index
        :param index: index名
        :return: 返回创建是否成功的信息
* deleteindex
>deleteindex(self, index):
        删除es中某个index
        :param index: index名
        :return: 返回删除是否成功的信息
* createmapping
>createmapping(self, index, mapping_body):
        在index目录下创建数据的mapping
        :param index: index名
        :param mapping_body: json格式的 mapping
        :return: 返回创建是否成功的结果
* ip_hits
>ip_hits(self, source_file_name, output_file_name, query_body):
        函数用来统计文件中ip在开源数据中命中次数
        :param source_file_name: 需要统计ip命中数的源文件
        :param output_file_name: 命中次数输出文件
        :param query_body: 查询结构
        :return:
