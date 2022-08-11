#!/bin/bash

aws ecs describe-services --region ap-east-1 --cluster Production --services p-authentication-api --query 'services[*].{ServiceArn:serviceArn,ServiceName:serviceName,Status:status,DesiredCount:desiredCount,RunningCount:runningCount,PendingCount:pendingCount,Events:events[:2]}'
