#coding:utf-8
#__author__ = '大婶N72'
import os
field_excel=[u'编号',u'接口名称',u'用例级别',u'请求类型',u'接口地址',u'接口头文件',u'接口请求参数',u'接口返回包',u'待比较参数',u'实际参数值',u'预期参数值',u'参数值比较结果',u'待比较参数集合',u'实际参数集合',u'参数完整性结果',u'用例状态',u'创建时间',u'更新时间']#导出的excel表格标题
src_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))#当前脚本所在目录的上级目录
#测试环境数据库配置，默认测试环境
host_test='127.0.0.1'
user_test='root'
password_test=''
name_test='test_interface'
port_test=3306
#生产环境数据库配置