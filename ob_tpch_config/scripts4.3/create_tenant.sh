# obclient -h127.0.0.1 -P1881 -uroot -p'123' -Doceanbase -c
# source sql/create_tenant.sql
echo sql/create_tenant.sql | obclient -h127.0.0.1 -P2881 -uroot -p'123' -Doceanbase -c > log2881.log || ret=1
