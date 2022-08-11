#!/bin/bash

aws ecs describe-services --region ap-east-1 --cluster Production --services p-address-api p-audit-log-api p-db-housekeeping-monthly --query 'services[*].{ServiceArn:serviceArn,ServiceName:serviceName,Status:status,DesiredCount:desiredCount,RunningCount:runningCount,PendingCount:pendingCount,Events:events[:2]}'
