zabbixzone:
    pkgrepo.managed:
    - humanname: CentOS $releasever - ZabbixZone
    - baseurl: http://repo.zabbixzone.com/centos/$releasever/$basearch/
    - gpgcheck: 1
    - gpgkey: http://repo.zabbixzone.com/centos/RPM-GPG-KEY-zabbixzone
    - require_in:
      - pkg: zabbix-agent

zabbixzone-noarch:
    pkgrepo.managed:
    - humanname: CentOS $releasever - ZabbixZone noarch
    - baseurl: http://repo.zabbixzone.com/centos/$releasever/noarch/
    - gpgcheck: 1
    - gpgkey: http://repo.zabbixzone.com/centos/RPM-GPG-KEY-zabbixzone
    - require_in:
      - pkg: zabbix-agent

zabbix-agent:
  pkg:
    - installed
  service:
    - running
    - require:
      - pkg: zabbix-agent
