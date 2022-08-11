#!/bin/bash

kubectl get deployments -n p-general p-db-housekeeping-monthly p-aggregation-api
kubectl get deployments -n p-authentication p-authentication-api
