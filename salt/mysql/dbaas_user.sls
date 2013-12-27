include:
  - mysql

{% if ( pillar['dbaas_api']['node']['status'] not in [9,10] ) and ( ( pillar['dbaas_api']['node']['status'] not in [3, 14, 15] ) or ( pillar['dbaas_api']['cluster']['status'] != 6 ) ) %}
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
    - grant: create, drop, lock tables, references, event, delete, index, insert, select, update, create temporary tables, trigger, create view, show view, alter routine, create routine, execute
    - database: {{ database }}.*
    - user: {{ pillar['dbaas_api']['cluster']['dbusername'] }}
    - host: '%'
    - require:
      - service: mysqld
{% endfor %}
{% endif %}
