include:
  - geniedb

update_subscriptions:
  module.wait:
    - connection_host: 'localhost'
    - connection_user: 'root'
    - connection_pass: ''
    - connection_port: {{ pillar['dbaas_api']['cluster']['port'] }}
    - connection_db: ''
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
