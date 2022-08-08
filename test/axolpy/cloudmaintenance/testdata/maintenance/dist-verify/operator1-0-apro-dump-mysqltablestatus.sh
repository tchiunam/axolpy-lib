#!/bin/bash

echo "database id: favorite"
mysql -h favorite.k3xsv7qtw4if.ap-east-1.rds.amazonaws.com -p 3306 -d favorite_v1 -U root -p -e 'show table status' -o favorite-tablestatus-`date +%Y%m%d-%H%M%S`.txt
echo "database id: bookmark"
mysql -h bookmark.k3xsv7qtw4if.ap-east-1.rds.amazonaws.com -p 3306 -d bookmark_v2 -U root -p -e 'show table status' -o bookmark-tablestatus-`date +%Y%m%d-%H%M%S`.txt
