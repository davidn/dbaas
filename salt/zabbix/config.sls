include:
  - zabbix

/etc/zabbix/zabbix_agentd.conf:
  file.managed:
    - show_diff: False
    - user: root
    - group: root
    - mode: 644
    - source:  salt://zabbix/zabbix_agentd.conf
    - template: jinja
    - watch_in:
      - service: zabbix-agent
