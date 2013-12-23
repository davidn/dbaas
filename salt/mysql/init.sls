mysql-server:
  pkg:
    - installed
mysqld:
  service:
# paused/pausing => shutdown mysql. The second condition allows leaving mysqld stopped during boot for nodes added after the cluster has started.
{% if ( pillar['dbaas_api']['node']['status'] in [9,10] ) or (pillar['dbaas_api']['node']['status'] == 3 and pillar['dbaas_api']['cluster']['status'] == 6) %}
    - dead
    - enable: False
{% else %}
    - running
    - enable: True
{% endif %}
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
