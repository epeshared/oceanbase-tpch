drop database if exists tpch_100g_qpl;
create database tpch_100g_qpl;
use tpch_100g_qpl;

DROP TABLEGROUP IF EXISTS tpch_tg_lineitem_order_group_qpl;
DROP TABLEGROUP IF EXISTS tpch_tg_partsupp_part_qpl;

CREATE TABLEGROUP IF NOT EXISTS tpch_tg_lineitem_order_group_qpl binding true partition by key 1 partitions 32;
CREATE TABLEGROUP IF NOT EXISTS tpch_tg_partsupp_part_qpl binding true partition by key 1 partitions 32;

DROP TABLE IF EXISTS lineitem;
CREATE TABLE lineitem (
  l_orderkey BIGINT NOT NULL,
  l_partkey BIGINT NOT NULL,
  l_suppkey INTEGER NOT NULL,
  l_linenumber INTEGER NOT NULL,
  l_quantity DECIMAL(15,2) NOT NULL,
  l_extendedprice DECIMAL(15,2) NOT NULL,
  l_discount DECIMAL(15,2) NOT NULL,
  l_tax DECIMAL(15,2) NOT NULL,
  l_returnflag char(1) DEFAULT NULL,
  l_linestatus char(1) DEFAULT NULL,
  l_shipdate date NOT NULL,
  l_commitdate date DEFAULT NULL,
  l_receiptdate date DEFAULT NULL,
  l_shipinstruct char(25) DEFAULT NULL,
  l_shipmode char(10) DEFAULT NULL,
  l_comment varchar(44) DEFAULT NULL,
  PRIMARY KEY(l_orderkey, l_linenumber))row_format = condensed
  tablegroup = tpch_tg_lineitem_order_group_qpl
  BLOCK_SIZE 65536
  partition by key (l_orderkey) partitions 32;

DROP TABLE IF EXISTS orders;
CREATE TABLE orders (
  o_orderkey bigint not null,
  o_custkey bigint not null,
  o_orderstatus char(1) default null,
  o_totalprice bigint default null,
  o_orderdate date not null,
  o_orderpriority char(15) default null,
  o_clerk char(15) default null,
  o_shippriority bigint default null,
  o_comment varchar(79) default null,
  PRIMARY KEY (o_orderkey))row_format = condensed
  tablegroup = tpch_tg_lineitem_order_group_qpl
  BLOCK_SIZE 65536
  partition by key(o_orderkey) partitions 32;

DROP TABLE IF EXISTS partsupp;
CREATE TABLE partsupp (
  ps_partkey bigint not null,
  ps_suppkey bigint not null,
  ps_availqty bigint default null,
  ps_supplycost bigint default null,
  ps_comment varchar(199) default null,
  PRIMARY KEY (ps_partkey, ps_suppkey))row_format = condensed
  tablegroup tpch_tg_partsupp_part_qpl
  BLOCK_SIZE 65536
  partition by key(ps_partkey) partitions 32;

DROP TABLE IF EXISTS part;
CREATE TABLE part (
  p_partkey bigint not null,
  p_name varchar(55) default null,
  p_mfgr char(25) default null,
  p_brand char(10) default null,
  p_type varchar(25) default null,
  p_size bigint default null,
  p_container char(10) default null,
  p_retailprice bigint default null,
  p_comment varchar(23) default null,
  PRIMARY KEY (p_partkey))row_format = condensed
  tablegroup tpch_tg_partsupp_part_qpl
  BLOCK_SIZE 65536
  partition by key(p_partkey) partitions 32;

DROP TABLE IF EXISTS customer;
CREATE TABLE customer (
  c_custkey bigint not null,
  c_name varchar(25) default null,
  c_address varchar(40) default null,
  c_nationkey bigint default null,
  c_phone char(15) default null,
  c_acctbal bigint default null,
  c_mktsegment char(10) default null,
  c_comment varchar(117) default null,
  PRIMARY KEY (c_custkey))row_format = condensed
  BLOCK_SIZE 65536
  partition by key(c_custkey) partitions 32;

DROP TABLE IF EXISTS supplier;
CREATE TABLE supplier (
  s_suppkey bigint not null,
  s_name char(25) default null,
  s_address varchar(40) default null,
  s_nationkey bigint default null,
  s_phone char(15) default null,
  s_acctbal bigint default null,
  s_comment varchar(101) default null,
  PRIMARY KEY (s_suppkey))row_format = condensed
  BLOCK_SIZE 65536
  partition by key(s_suppkey) partitions 32;

DROP TABLE IF EXISTS nation;
CREATE TABLE nation (
  n_nationkey bigint not null,
  n_name char(25) default null,
  n_regionkey bigint default null,
  n_comment varchar(152) default null,
  PRIMARY KEY (n_nationkey))row_format = condensed
  BLOCK_SIZE 65536;

DROP TABLE IF EXISTS region;
CREATE TABLE region (
  r_regionkey bigint not null,
  r_name char(25) default null,
  r_comment varchar(152) default null,
  PRIMARY KEY (r_regionkey))row_format = condensed
  BLOCK_SIZE 65536;

