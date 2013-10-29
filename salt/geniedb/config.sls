include:
  - geniedb

update_subscriptions:
  module.wait:
    - name: mysql.query
    - database: test
    - query: SET GLOBAL geniedb_subscriptions="{{pillar['dbaas_api']['cluster']['subscriptions']}}";
    - watch:
      - file: /etc/mysql/conf.d/geniedb.cnf

/etc/mysql/conf.d/geniedb.cnf:
  file.managed:
    - makedirs: True
    - source: salt://geniedb/geniedb.cnf
    - template: jinja
    - require_in:
      - service: mysqld
