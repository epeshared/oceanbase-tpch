create resource unit tpch_unit max_cpu 16, memory_size '30g',MIN_CPU 16,log_disk_size '10g';
create resource pool tpch_pool unit = 'tpch_unit', unit_num = 1, zone_list=('zone1');
create tenant tpch_mysql resource_pool_list=('tpch_pool'), zone_list('zone1'), primary_zone=RANDOM, locality='F@zone1' set variables ob_compatibility_mode='mysql', ob_tcp_invited_nodes='%';
