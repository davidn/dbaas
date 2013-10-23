include:
  - mysql

db_user:
  mysql_user.present:
    - name: {{ pillar['dbaas_api']['cluster']['dbusername'] }}
    - host: '%'
    - password: {{ pillar['dbaas_api']['cluster']['dbpassword'] }}

database:
  mysql_database.present:
    - name: {{ pillar['dbaas_api']['cluster']['dbname'] }}

user_to_db:
  mysql_grants.present:
    - grant: all privileges
    - database: {{ pillar['dbaas_api']['cluster']['dbname'] }}.*
    - user: {{ pillar['dbaas_api']['cluster']['dbusername'] }}
