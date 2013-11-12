/etc/mysqlbackup.logrotate:
  file.managed:
    - show_diff: False
    - source: salt://backup/mysqlbackup.logrotate
    - user: root
    - group: root
    - mode: 644
    - template: jinja
    - require:
      - file: /usr/local/bin/backup

/usr/local/bin/backup:
  cron.present:
    - user: root
    - minute: '{{ pillar['dbaas_api']['cluster']['backup_parts'][0] }}'
    - hour: '{{ pillar['dbaas_api']['cluster']['backup_parts'][1] }}'
    - daymonth: '{{ pillar['dbaas_api']['cluster']['backup_parts'][2] }}'
    - month: '{{ pillar['dbaas_api']['cluster']['backup_parts'][3] }}'
    - dayweek: '{{ pillar['dbaas_api']['cluster']['backup_parts'][4] }}'
    - require:
      - pkg: s3cmd
      - file: /root/.s3cfg
  file.managed:
    - show_diff: False
    - source: salt://backup/backup.sh
    - user: root
    - group: root
    - mode: 755
    - template: jinja
