1. 创建实例 \
    obd cluster deploy ob_ins1 -c ob_config.yaml \
    obd cluster start ob_ins1 
2. 参数配置 \
  2.1 创建租户 \
  create resource unit tpch_unit max_cpu 16, memory_size '50g',MIN_CPU 16,log_disk_size '30g'; \
  create resource pool tpch_pool unit = 'tpch_unit', unit_num = 1, zone_list=('zone1'); \
  create tenant tpch_mysql resource_pool_list=('tpch_pool'),  zone_list('zone1'), primary_zone=RANDOM, 
  locality='F@zone1' set variables ob_compatibility_mode='mysql', ob_tcp_invited_nodes='%'; \
  2.2 系统参数 \
  alter system set enable_sql_audit=False; \
  alter system set enable_sql_extension=True tenant=tpch_mysql; \
  alter system set syslog_level='PERF'; \
  alter system set max_syslog_file_count=100; \
  alter system set trace_log_slow_query_watermark='100s'; \
  alter system set _hash_area_size='3g' tenant=tpch_mysql; \
  alter system set enable_rebalance=False; \
  alter system set cache_wash_threshold='30g'; \
  alter system set ob_enable_batched_multi_statement=True tenant=tpch_mysql; \
  alter system set _bloom_filter_ratio=10; \
  alter system set _rowsets_enabled=True tenant=tpch_mysql; \
  alter system set disk_io_thread_count = 32; \
  alter system set _parallel_server_sleep_time=10; \
  alter system set cpu_quota_concurrency=4; \
  alter system set syslog_io_bandwidth_limit='30m'; \
  alter system set enable_async_syslog=True; \
  alter system set large_query_worker_percentage=10; \
  alter system set builtin_db_data_verify_cycle=0; \
  alter system set micro_block_merge_verify_level=0; \
  alter system set freeze_trigger_percentage=50; \
  alter system set enable_perf_event=False; \
  alter system set large_query_threshold='1s'; \
  alter system flush plan cache global; \
  alter system set _io_callback_thread_count =16; \
  GRANT ALL PRIVILEGES ON \*.\* TO 'root'@'%' IDENTIFIED BY '123';
  
  alter system set  default_compress_func = 'zlib_lite_1.0'; \
 /* alter system set  default_compress_func = 'lz4_1.0'; \
  alter system set  default_compress_func = 'zstd_1.3.8';*/ \
  
  2.3 切换到租户，配置参数 \
  set global ob_sql_work_area_percentage = 80; \
  set global optimizer_use_sql_plan_baselines = True; \
  set global optimizer_capture_sql_plan_baselines = True; \
  set global ob_query_timeout = 36000000000; \
  set global ob_trx_timeout = 36000000000; \
  set global max_allowed_packet = 67108864; \
  set global parallel_servers_target = 896; \
  set global _groupby_nopushdown_cut_ratio = 1; \
 \
  CREATE USER tpch IDENTIFIED BY password '*e9c2bcdc178a99b7b08dd25db58ded2ee5bff050' ;  \
  grant all privileges on \*.\* to tpch@'%' identified by '123'; \
 \
3. 参数配置成功后，需要重启实例 \
4. 导入数据 \
   python3 load.py \
5. 导入数据后，需要执行以下SQL \
  root@tpch \
  alter system major freeze tenant=tpch_mysql; \
  select FROZEN_SCN, LAST_SCN from oceanbase.CDB_OB_MAJOR_COMPACTION; \
 \
  use tpch_100g_qpl; \
  set _force_parallel_query_dop = 112; \
  analyze table lineitem partition(lineitem) compute statistics for all columns size auto;  \
  analyze table orders partition(orders) compute statistics for all columns size auto;  \
  analyze table partsupp partition(partsupp) compute statistics for all columns size auto;  \
  analyze table part partition(part) compute statistics for all columns size auto;  \
  analyze table customer partition(customer) compute statistics for all columns size auto;  \
  analyze table supplier partition(supplier) compute statistics for all columns size auto;  \
  analyze table nation compute statistics for all columns size auto;  \
  analyze table region compute statistics for all columns size auto; \
6. 测试 \
  python3 multi_ins_test.py \

7.如果导入数据出现权限问题，执行该命令 \
obclient -S ob_data/run/sql.sock  -utpch@tpch_mysql -p123 -e "set global secure_file_priv = '/';" 

8.创建表的ddl文件中，BLOCK_SIZE 65536，性能最好， partitions 32 最好和可用cpu数量一致，在8C16T的情况下，32性能要更好一些，db.sql /*parallel(16)*/,一般和可用cpu数量一致。 \
 \
参考 \
https://www.oceanbase.com/docs/common-oceanbase-database-cn-0000000001953497 \
