include:
  - mysql

{% if ( pillar['dbaas_api']['node']['status'] not in [9,10, 1001] ) and ( ( pillar['dbaas_api']['node']['status'] not in [3, 14, 15] ) or ( pillar['dbaas_api']['cluster']['status'] != 6 ) ) %}
db_user:
  mysql_user.present:
    - connection_host: 'localhost'
    - connection_user: 'root'
    - connection_pass: ''
    - connection_port: {{ pillar['dbaas_api']['cluster']['port'] }}
    - connection_db: ''
    - name: {{ pillar['dbaas_api']['cluster']['dbusername'] }}
    - host: '%'
    - password: {{ pillar['dbaas_api']['cluster']['dbpassword'] }}
    - require:
      - service: mysqld

{% for database in pillar['dbaas_api']['cluster']['dbname_parts'] %}
database_{{database}}:
  mysql_database.present:
    - connection_host: 'localhost'
    - connection_user: 'root'
    - connection_pass: ''
    - connection_port: {{ pillar['dbaas_api']['cluster']['port'] }}
    - connection_db: ''
    - name: {{ database }}
    - require:
      - service: mysqld

user_to_db_{{database}}:
  mysql_grants.present:
    - connection_host: 'localhost'
    - connection_user: 'root'
    - connection_pass: ''
    - connection_port: {{ pillar['dbaas_api']['cluster']['port'] }}
    - connection_db: ''
    - grant: SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, REFERENCES, INDEX, CREATE TEMPORARY TABLES, LOCK TABLES, EXECUTE, CREATE VIEW, SHOW VIEW, CREATE ROUTINE, ALTER ROUTINE, EVENT, TRIGGER
    - database: {{ database }}.*
    - user: {{ pillar['dbaas_api']['cluster']['dbusername'] }}
    - host: '%'
    - require:
      - service: mysqld
      - mysql_database: database_{{database}}
      - mysql_user: db_user
{% endfor %}
{% endif %}
