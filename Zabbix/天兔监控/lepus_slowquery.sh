#!/bin/bash
#****************************************************************#
# ScriptName: /usr/local/sbin/lepus_slowquery.sh
# Create Date: 2014-03-25 10:01
# Modify Date: 2014-03-25 10:01
#***************************************************************#

#config lepus database server
lepus_db_host="10.43.112.184"
lepus_db_port=3306
lepus_db_user="root"
lepus_db_password="Qq12345678%"
lepus_db_database="lepus"

#config mysql server
mysql_client="/home/data/mysql/bin/mysql"
mysql_host="127.0.0.1"
mysql_port=3306
mysql_user="root"
mysql_password="Pdmi1234!"

#config slowqury
slowquery_dir="/home/data/mysql/logs/"
slowquery_long_time=5
slowquery_file=`$mysql_client -h$mysql_host -P$mysql_port -u$mysql_user -p$mysql_password  -e "show variables like 'slow_query_log_file'"|grep log|awk '{print $2}'`
pt_query_digest="/usr/bin/pt-query-digest"

#config server_id
lepus_server_id=183

#collect mysql slowquery log into lepus database
$pt_query_digest --user=$lepus_db_user --password=$lepus_db_password --port=$lepus_db_port --review h=$lepus_db_host,D=$lepus_db_database,t=mysql_slow_query_review  --history h=$lepus_db_host,D=$lepus_db_database,t=mysql_slow_query_review_history  --no-report --limit=100% --filter=" \$event->{add_column} = length(\$event->{arg}) and \$event->{serverid}=$lepus_server_id " $slowquery_file > /tmp/lepus_slowquery.log

##### set a new slow query log ###########
tmp_log=`$mysql_client -h$mysql_host -P$mysql_port -u$mysql_user -p$mysql_password -e "select concat('$slowquery_dir','slowquery_',date_format(now(),'%Y%m%d%H'),'.log');"|grep log|sed -n -e '2p'`

#config mysql slowquery
$mysql_client -h$mysql_host -P$mysql_port -u$mysql_user -p$mysql_password -e "set global slow_query_log=1;set global long_query_time=$slowquery_long_time;"
$mysql_client -h$mysql_host -P$mysql_port -u$mysql_user -p$mysql_password -e "set global slow_query_log_file = '$tmp_log'; "

#delete log before 7 days
cd $slowquery_dir
/usr/bin/find ./ -name 'slowquery_*' -mtime +7|xargs rm -rf ;

####END####

