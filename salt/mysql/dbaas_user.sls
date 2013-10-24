include:
  - mysql

db_user:
  mysql_user.present:
    - name: {{ pillar['dbaas_api']['cluster']['dbusername'] }}
    - host: '%'
    - password: {{ pillar['dbaas_api']['cluster']['dbpassword'] }}
    - require:
      - service: mysqld

{% for database in pillar['dbaas_api']['cluster']['dbname_parts'] %}
database_{{database}}:
  mysql_database.present:
    - name: {{ database }}
    - require:
      - service: mysqld

user_to_db_{{database}}:
  mysql_grants.present:
    - grant: all privileges
    - database: {{ database }}.*
    - user: {{ pillar['dbaas_api']['cluster']['dbusername'] }}
    - require:
      - service: mysqld
{% endfor %}
