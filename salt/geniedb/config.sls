include:
  - geniedb

/etc/mysql/conf.d/geniedb.cnf:
  file.managed:
    - makedirs: True
    - source: salt://geniedb/geniedb.cnf
    - template: jinja
