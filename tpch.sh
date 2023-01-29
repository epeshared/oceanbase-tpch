#!/bin/bash
host_ip=127.0.0.1
host_port=2881
user=root
tenant=tpch_test
database=tpch_100G
passward=''
TPCH_TEST="obclient -h $host_ip -P $host_port -u$user@$tenant  -D $database -c"
echo $TPCH_TEST
echo $TPCH_TEST
#warmup预热
#for i in {1..22}
#do
#    sql1="source db${i}.sql"
#    echo $sql1
#    echo $sql1| $TPCH_TEST >db${i}.log  || ret=1
#done
#正式执行
for i in {1..20}
do
    rm -rf *.csv
    rm -rf *.dat
    rm -rf summary_q${i}.xlsx
    starttime=`date +%s%N`
    echo `date  '+[%Y-%m-%d %H:%M:%S]'` "BEGIN Q${i}"
    sql1="source db${i}.sql"
    emon -collect-edp > emon.dat &
    echo $sql1| $TPCH_TEST >db${i}.log  || ret=1
    stoptime=`date +%s%N`
    emon -stop
    costtime=`echo $stoptime $starttime | awk '{printf "%0.2f\n", ($1 - $2) / 1000000000}'`
    echo `date  '+[%Y-%m-%d %H:%M:%S]'` "END,COST ${costtime}s"
    emon -process-edp /opt/intel/emon/config/edp/edp_config.txt
    mv summary.xlsx  summary_q${i}.xlsx
    rm -rf *.csv
    rm -rf *.dat
done
