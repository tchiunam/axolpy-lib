#!/bin/bash

aws rds describe-db-instances --region ap-east-1 --db-instance-identifier audit_log --query 'DBInstances[*].{DBInstanceIdentifier:DBInstanceIdentifier,DBInstanceClass:DBInstanceClass,Engine:Engine,DBInstanceStatus:DBInstanceStatus,DBName:DBName,Endpoint:Endpoint,EngineVersion:EngineVersion}'
sleep 2
aws rds describe-db-instances --region ap-east-1 --db-instance-identifier subcription --query 'DBInstances[*].{DBInstanceIdentifier:DBInstanceIdentifier,DBInstanceClass:DBInstanceClass,Engine:Engine,DBInstanceStatus:DBInstanceStatus,DBName:DBName,Endpoint:Endpoint,EngineVersion:EngineVersion}'
