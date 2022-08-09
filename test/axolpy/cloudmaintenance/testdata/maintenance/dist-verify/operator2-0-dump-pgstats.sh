#!/bin/bash

echo "database id: audit_log"
psql -h audit_log.k3xsv7qtw4if.ap-east-1.rds.amazonaws.com -p 5432 -d audit_log -U postgres -W -c 'select * from pg_stat_all_tables order by schemaname, relname' -o audit_log-pg_stat-`date +%Y%m%d-%H%M%S`.csv
echo "database id: subcription"
psql -h subscription.k3xsv7qtw4if.ap-east-1.rds.amazonaws.com -p 5432 -d subscription_v1 -U postgres -W -c 'select * from pg_stat_all_tables order by schemaname, relname' -o subcription-pg_stat-`date +%Y%m%d-%H%M%S`.csv
