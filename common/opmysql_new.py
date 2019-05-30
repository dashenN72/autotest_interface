#__author__ = 'hrwang'
# -*- coding:utf-8 -*-
'''
定义对mysql数据库基本操作的封装
1.包括基本的单条语句操作，删除、修改、更新
2.独立的查询单条、查询多条数据
3.独立的添加多条数据
'''
import logging,os,pymysql
from public import config
#读取配置文件数据库配置
DBHOST=config.host_test
DBUSER=config.user_test
DBPASSWD=config.password_test
DBNAME=config.name_test
DBPORT=config.port_test


class OperationDbInterface(object):
    def __init__(self):
        self.dbname=DBHOST
        self.dbuser=DBUSER
        self.dbpasswd=DBPASSWD
        self.dbport=DBPORT
        self.dbhost=DBHOST

    def connect_sql(self):
        if self.dbhost:
            pass
        else:
            pass


    def __init__(self,host_db='192.168.0.103',user_db='root',passwd_db='root',name_db='test_interface',port_db=3306,link_type=0):
        '''
        :param host_db: 数据库服务主机
        :param user_db: 数据库用户名
        :param passwd_db: 数据库密码
        :param name_db: 数据库名称
        :param port_db: 端口号，整型数字
        :param link_type: 链接类型，用于输出数据是元祖还是字典，默认是字典，link_type=0
        :return:游标
        '''
        try:
            if link_type == 0:
                self.conn=pymysql.connect(host=host_db,user=user_db, passwd=passwd_db, db=name_db, port=port_db,
                                          charset='utf8',cursorclass = pymysql.cursors.DictCursor)#创建数据库链接,返回字典
            else:
                self.conn = pymysql.connect(host=host_db, user=user_db, passwd=passwd_db, db=name_db, port=port_db,
                                            charset='utf8')  # 创建数据库链接，返回元祖
            self.cur=self.conn.cursor()
        except pymysql.Error as e:
            print("创建数据库连接失败|Mysql Error %d: %s" % (e.args[0], e.args[1]))
            logging.basicConfig(filename = config.src_path + '/log/syserror.log',level = logging.DEBUG,format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
            logger = logging.getLogger(__name__)
            logger.exception(e)
    #定义单条数据操作，包含删除、更新操作
    def op_sql(self,condition):
        '''
        :param condition: sql语句,该通用方法可用来替代updateone，deleteone
        :return:字典形式
        '''
        try:
            self.cur.execute(condition)#执行sql语句
            self.conn.commit()#提交游标数据
            result={'code':'0000','message':'执行通用操作成功','data':[]}
        except pymysql.Error as e:
            self.conn.rollback()  # 执行回滚操作
            result={'code':'9999','message':'执行通用操作异常','data':[]}
            print (u"数据库错误|op_sql %d: %s" % (e.args[0], e.args[1]))
            logging.basicConfig(filename = os.path.join(os.getcwd(), config.src_path + '/log/syserror.log'), level = logging.DEBUG, format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
            logger = logging.getLogger(__name__)
            logger.exception(e)
        return result

        # 查询表中单条数据
    def select_one(self, condition):
        '''
        :param condition: sql语句
        :return:字典形式的单条查询结果
        '''
        try:
            rows_affect = self.cur.execute(condition)
            if rows_affect > 0:  # 查询结果返回数据数大于0
                results = self.cur.fetchone()  # 获取一条结果
                result = {'code': '0000', 'message': '执行单条查询操作成功', 'data': results}
            else:
                result = {'code': '0000', 'message': '执行单条查询操作成功', 'data': []}
        except pymysql.Error as e:
            self.conn.rollback()  # 执行回滚操作
            result = {'code': '9999', 'message': '执行单条查询异常', 'data': []}
            print (u"数据库错误|select_one %d: %s" % (e.args[0], e.args[1]))
            logging.basicConfig(filename=os.path.join(os.getcwd(), config.src_path + '/log/syserror.log'), level=logging.DEBUG,
                                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
            logger = logging.getLogger(__name__)
            logger.exception(e)
        return result
    #查询表中多条数据
    def select_all(self,condition):
        '''
        :param condition: sql语句
        :return:字典形式的批量查询结果
        '''
        try:
            rows_affect=self.cur.execute(condition)
            if rows_affect>0:#查询结果返回数据数大于0
                self.cur.scroll(0, mode='absolute') # 光标回到初始位置
                results = self.cur.fetchall()#返回游标中所有结果
                result={'code':'0000','message':'执行批量查询操作成功','data':results}
            else:
                result={'code':'0000','message':'执行批量查询操作成功','data':[]}
        except pymysql.Error as e:
            self.conn.rollback()  # 执行回滚操作
            result={'code':'9999','message':'执行批量查询异常','data':[]}
            print (u"数据库错误|select_all %d: %s" % (e.args[0], e.args[1]))
            logging.basicConfig(filename = os.path.join(os.getcwd(), config.src_path + '\log\syserror.log'), level = logging.DEBUG, format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
            logger = logging.getLogger(__name__)
            logger.exception(e)
        return result
    #定义表中插入数据操作
    def insert_data(self,condition,params):
        '''
        :param condition: insert语句
        :param params: insert数据，列表形式[('3','Tom','1 year 1 class','6'),('3','Jack','2 year 1 class','7'),]
        :return:字典形式的批量插入数据结果
        '''
        try:
            results=self.cur.executemany(condition,params)#返回插入的数据条数
            self.conn.commit()
            result={'code':'0000','message':'执行批量查询操作成功','data':int(results)}
        except pymysql.Error as e:
            self.conn.rollback()  # 执行回滚操作
            result={'code':'9999','message':'执行批量插入异常','data':[]}
            print (u"数据库错误|insert_more %d: %s" % (e.args[0], e.args[1]))
            logging.basicConfig(filename = os.path.join(os.getcwd(), config.src_path + '/log/syserror.log'), level = logging.DEBUG, format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
            logger = logging.getLogger(__name__)
            logger.exception(e)
        return result
    #数据库关闭
    def __del__(self):
        if self.cur != None:
            self.cur.close()#关闭游标
        if self.conn != None:
            self.conn.close()#释放数据库资源
if __name__ == "__main__":
    test=OperationDbInterface()#实例化类
    result_select_all=test.select_all("SELECT * FROM config_total")#查询多条数据
    result_select_one=test.select_one("SELECT * FROM config_total WHERE id=2")#查询单条数据
    result_op_sql=test.op_sql("update test_xml set xml='test' WHERE id=1")#通用操作
    result=test.insert_data("insert into test_xml(xml) values (%s)",[('mytest11'),('mytest22')])#插入操作
    #result=test.insertMore("insert into config_total(key_config,value_config,status) values(%s,%s,%s)",[(1,1,1),(2,2,2)])
    print(result_select_all['data'], result_select_all['message'])
    print(result_select_one['data'], result_select_one['message'])
    print(result_op_sql['data'], result_op_sql['message'])
    print(result['data'], result['message'])
    # if result['code']=='0000':
    #     print(result['data'],result['message'])
    # else:
    #     print(result['message'])