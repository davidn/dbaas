include:
  - zabbix

/etc/zabbix/zabbix_agentd.conf:
  file.managed:
    - user: root
    - group: root
    - mode: 644
    - source:  salt://zabbix/zabbix_agentd.conf
    - template: jinja
