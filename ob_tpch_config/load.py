import os
import sys
import time
import subprocess
hostname='127.0.0.1'   # 注意！！请填写某个 observer，如 observer A 所在服务器的 IP 地址
port='3881'               # observer A 的端口号
tenant='tpch_mysql'              # 租户名
user='tpch'               # 用户名
password='123'           # 密码
data_path='/mnt/md127/ob_test/100G'         # 注意！！请填写 observer A 所在服务器下 tbl 所在目录
 
 
cmd_str=""" mysql -h%s -P%s -uroot -p%s  -e "alter system set  default_compress_func = 'zlib_lite_1.0';" """ %(hostname,port,password)
result = subprocess.getstatusoutput(cmd_str) 
cmd_str='mysql -h%s -P%s -u%s@%s -p%s < create_tpch_mysql_table_part.ddl'%(hostname,port,user,tenant,password)
result = subprocess.getstatusoutput(cmd_str)
print(result)
cmd_str='mysql -h%s -P%s -u%s@%s -p%s  -D%s -e "show tables;" '%(hostname,port,user,tenant,password,db_name)
result = subprocess.getstatusoutput(cmd_str)
print(result)
cmd_str=""" mysql -h%s -P%s -u%s@%s -p%s -c  -D%s -e "load data /*+ parallel(80) */ infile '%s/customer.tbl' into table customer fields terminated by '|';" """ %(hostname,port,user,tenant,password,db_name,data_path)
result = subprocess.getstatusoutput(cmd_str)
print(result)
cmd_str=""" mysql -h%s -P%s -u%s@%s -p%s -c  -D%s -e "load data /*+ parallel(80) */ infile '%s/lineitem.tbl' into table lineitem fields terminated by '|';" """ %(hostname,port,user,tenant,password,db_name,data_path)
result = subprocess.getstatusoutput(cmd_str)
print(result)
cmd_str=""" mysql -h%s -P%s -u%s@%s -p%s -c -D%s -e "load data /*+ parallel(80) */ infile '%s/nation.tbl' into table nation fields terminated by '|';" """ %(hostname,port,user,tenant,password,db_name,data_path)
result = subprocess.getstatusoutput(cmd_str)
print(result)
cmd_str=""" mysql -h%s -P%s -u%s@%s -p%s -c  -D%s -e "load data /*+ parallel(80) */ infile '%s/orders.tbl' into table orders fields terminated by '|';" """ %(hostname,port,user,tenant,password,db_name,data_path)
result = subprocess.getstatusoutput(cmd_str)
print(result)
cmd_str=""" mysql -h%s -P%s -u%s@%s -p%s   -D%s -e "load data /*+ parallel(80) */ infile '%s/partsupp.tbl' into table partsupp fields terminated by '|';" """ %(hostname,port,user,tenant,password,db_name,data_path)
result = subprocess.getstatusoutput(cmd_str)
print(result)
cmd_str=""" mysql -h%s -P%s -u%s@%s -p%s -c  -D%s -e "load data /*+ parallel(80) */ infile '%s/part.tbl' into table part fields terminated by '|';" """ %(hostname,port,user,tenant,password,db_name,data_path)
result = subprocess.getstatusoutput(cmd_str)
print(result)
cmd_str=""" mysql -h%s -P%s -u%s@%s -p%s -c  -D%s -e "load data /*+ parallel(80) */ infile '%s/region.tbl' into table region fields terminated by '|';" """ %(hostname,port,user,tenant,password,db_name,data_path)
result = subprocess.getstatusoutput(cmd_str)
print(result)
cmd_str=""" mysql -h%s -P%s -u%s@%s -p%s -c  -D%s -e "load data /*+ parallel(80) */ infile '%s/supplier.tbl' into table supplier fields terminated by '|';" """ %(hostname,port,user,tenant,password,db_name,data_path)
result = subprocess.getstatusoutput(cmd_str)
