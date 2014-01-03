#!/bin/sh
UP=$(/usr/bin/mysql -e 'status'  | wc -l);
if [ "$UP" -ge 1 ];
then
        /usr/bin/mysqldump --all-databases > /var/backup/mysqlbackup.sql
        /usr/sbin/logrotate -fs /etc/mysqlbackup.state /etc/mysqlbackup.logrotate
else
        exit
fi
/usr/bin/s3cmd sync --delete-removed /var/backup/ s3://{{pillar['dbaas_api']['settings']['BUCKET_NAME']}}/{{pillar['dbaas_api']['cluster']['uuid']}}/{{pillar['dbaas_api']['node']['nid']}}/




/usr/bin/curl {{pillar['dbaas_api']['node']['set_backup_url']}} -X POST -H "Content-type: application/json" -d "$(
  c=false
  cd /var/backup/
  printf '[\n'
  for i in *; do
    if $c; then
      printf ',\n'
    else
      c=true
    fi
    stat --printf '  {"filename":"%n", "time":"%y", "size":"%s"}' "$i"
  done


  printf '\n]\n'
)"
