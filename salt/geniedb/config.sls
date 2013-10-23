include:
  - geniedb

/etc/my.cnf:
  file.append:
    - text: |
        !includedir /etc/mysql/conf.d/

/etc/mysql/conf.d/geniedb.cnf:
  file.managed:
    - makedirs: True
    - source: salt://geniedb/geniedb.cnf
    - template: jinja
