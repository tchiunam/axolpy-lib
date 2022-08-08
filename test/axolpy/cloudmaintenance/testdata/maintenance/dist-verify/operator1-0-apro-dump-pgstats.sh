#!/bin/bash

echo "database id: user"
psql -h user.k3xsv7qtw4if.ap-east-1.rds.amazonaws.com -p 5432 -d user -U postgres -W -c 'select * from pg_stat_all_tables order by schemaname, relname' -o user-pg_stat-`date +%Y%m%d-%H%M%S`.csv
echo "database id: address"
psql -h address.k3xsv7qtw4if.ap-east-1.rds.amazonaws.com -p 5432 -d address -U postgres -W -c 'select * from pg_stat_all_tables order by schemaname, relname' -o address-pg_stat-`date +%Y%m%d-%H%M%S`.csv
