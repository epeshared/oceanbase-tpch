import re
import os
import time
import _thread  as thread
import random

TPCH_SQL= [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22]
SQL_TOTAL_NUM=22
TPCH_CLIENT = 7
CLIENT_START_NUM=[1,1,1,1,1,1,1,1]
OB_PORT = [3881,4881,5881,6881,7881,8881,9881,10881]
ALL_result={}
def warmup(threadname,client):
    print("%s warmup begin" % threadname)  
    for i in TPCH_SQL:
        ob_connect =  "mysql -h 127.0.0.1 -P  %d  -utpch@tpch_mysql  -D tpch_100g_qpl -p123 -c " % OB_PORT[client]
        sql_commond = " source sql/db%d.sql " %i
        excute_commond = "echo" + sql_commond + "|" + ob_connect + " > log/" + str(client) + "/db" + str(i) + ".log" + " || ret=1"
        os.system(excute_commond)
    print("%s warmup done" % threadname)

def excute_sql(threadname,client):
    #warmup预热
    warmup(threadname,client)

    iter=1
    current_sql=CLIENT_START_NUM[client]
    print(threadname + " work begin ")
    thread_result={}
    while iter <= SQL_TOTAL_NUM:
        ob_connect =  "mysql -h 127.0.0.1 -P  %d  -utpch@tpch_mysql  -D tpch_100g_qpl -p123 -c " % OB_PORT[client]
        current_sql=current_sql%SQL_TOTAL_NUM
        if current_sql == 0:
            current_sql=SQL_TOTAL_NUM
        sql_commond = " source sql/db%d.sql " % current_sql
        excute_commond = "echo" + sql_commond + "|" + ob_connect + " > log/" + str(client) + "/db" + str(current_sql) + ".log" + " || ret=1"
        start_time = time.time()
        os.system(excute_commond)
        # time.sleep(1)
        end_time = time.time()
        cost = round(end_time - start_time,2)
        thread_result[current_sql]=cost

        iter +=1
        current_sql +=1

    ALL_result[client]=thread_result
    print(thread_result)

def analysis_data():
    print("analysis data begin")
    client = 0
    while client <= TPCH_CLIENT:
        print(str(client) + "_thread_client" + " show begin ")
        for elem in sorted (ALL_result[client]):
            print('SQL:%-10s  %-3.2f' % (str(elem),  ALL_result[client][elem]), end =" \n")
        print(str(client) + "_thread_client" + " show end ")
        client += 1
    print("analysis data done")

if __name__ == "__main__":
    #测试
    client = 0
    while client <= TPCH_CLIENT:
        thread_name = "client_%d" % client
        thread.start_new_thread(excute_sql, (thread_name,client))
        client += 1
        
    while 1:
        if len(ALL_result) == (TPCH_CLIENT+1):
            analysis_data()
            break 
        else:
            time.sleep(10)
    


    
