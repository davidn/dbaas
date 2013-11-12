mysql-server:
  pkg:
    - installed
mysqld:
  service:
{% if pillar['dbaas_api']['node']['status'] in [9,10] %}
    - dead
{% else %}
    - running
{% endif %}
    - enable: True
    - require:
      - pkg: mysql-server

/etc/my.cnf:
  file.append:
    - text: |
        !includedir /etc/mysql/conf.d/

/etc/mysql/conf.d/custom.cnf:
  file.managed:
    - show_diff: False
    - makedirs: True
    - source: salt://mysql/custom.cnf
    - template: jinja
    - watch_in:
      - service: mysqld

/etc/mysql/ca.cert:
  file.managed:
    - show_diff: False
    - makedirs: True
    - source: salt://mysql/ca.cert
    - template: jinja
    - watch_in:
      - service: mysqld

/etc/mysql/server.cert:
  file.managed:
    - show_diff: False
    - makedirs: True
    - source: salt://mysql/server.cert
    - template: jinja
    - watch_in:
      - service: mysqld

/etc/mysql/server.pem:
  file.managed:
    - show_diff: False
    - makedirs: True
    - source: salt://mysql/server.pem
    - template: jinja
    - watch_in:
      - service: mysqld
