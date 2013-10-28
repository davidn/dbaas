mysql-server:
  pkg:
    - installed
mysqld:
  service:
    - running
    - enable: True
    - require:
      - pkg: mysql-server

/etc/my.cnf:
  file.append:
    - text: |
        !includedir /etc/mysql/conf.d/

/etc/mysql/conf.d/custom.cnf:
  file.managed:
    - makedirs: True
    - source: salt://mysql/custom.cnf
    - template: jinja
    - watch_in:
      - service: mysqld

/etc/mysql/ca.cert:
  file.managed:
    - makedirs: True
    - source: salt://mysql/ca.cert
    - template: jinja
    - watch_in:
      - service: mysqld

/etc/mysql/server.cert:
  file.managed:
    - makedirs: True
    - source: salt://mysql/server.cert
    - template: jinja
    - watch_in:
      - service: mysqld

/etc/mysql/server.pem:
  file.managed:
    - makedirs: True
    - source: salt://mysql/server.pem
    - template: jinja
    - watch_in:
      - service: mysqld
