#!/bin/bash

aws rds describe-db-instances --region ap-east-1 --db-instance-identifier user --query 'DBInstances[*].{DBInstanceIdentifier:DBInstanceIdentifier,DBInstanceClass:DBInstanceClass,Engine:Engine,DBInstanceStatus:DBInstanceStatus,DBName:DBName,Endpoint:Endpoint,EngineVersion:EngineVersion}'
sleep 2
aws rds describe-db-instances --region ap-east-1 --db-instance-identifier address --query 'DBInstances[*].{DBInstanceIdentifier:DBInstanceIdentifier,DBInstanceClass:DBInstanceClass,Engine:Engine,DBInstanceStatus:DBInstanceStatus,DBName:DBName,Endpoint:Endpoint,EngineVersion:EngineVersion}'
sleep 2
aws rds describe-db-instances --region ap-east-1 --db-instance-identifier favorite --query 'DBInstances[*].{DBInstanceIdentifier:DBInstanceIdentifier,DBInstanceClass:DBInstanceClass,Engine:Engine,DBInstanceStatus:DBInstanceStatus,DBName:DBName,Endpoint:Endpoint,EngineVersion:EngineVersion}'
sleep 2
aws rds describe-db-instances --region ap-east-1 --db-instance-identifier bookmark --query 'DBInstances[*].{DBInstanceIdentifier:DBInstanceIdentifier,DBInstanceClass:DBInstanceClass,Engine:Engine,DBInstanceStatus:DBInstanceStatus,DBName:DBName,Endpoint:Endpoint,EngineVersion:EngineVersion}'
