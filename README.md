# oceanbase-tpch

系统租户
alter system set system_memory='15g';
alter resource unit sys_unit_config max_memory='15g',min_memory='15g';
alter system set enable_merge_by_turn= False;
alter system set trace_log_slow_query_watermark='100s';
alter system set max_kept_major_version_number=1;
alter system set enable_sql_operator_dump=True;
alter system set _hash_area_size='3g';
alter system set memstore_limit_percentage=50;
alter system set enable_rebalance=False;
alter system set memory_chunk_cache_size='1g';
alter system set minor_freeze_times=5;
alter system set merge_thread_count=20;
alter system set cache_wash_threshold='30g';
alter system set syslog_level='PERF';
alter system set max_syslog_file_count=100;
alter system set enable_syslog_recycle='True';


设置租户
set global ob_sql_work_area_percentage=80;
set global optimizer_use_sql_plan_baselines = true;
set global optimizer_capture_sql_plan_baselines = true;
alter system set ob_enable_batched_multi_statement='true';
set global ob_query_timeout=36000000000;
set global ob_trx_timeout=36000000000;
set global max_allowed_packet=67108864;
set global secure_file_priv="";


                                          
grant file on *.* to tpch_100g_part;
