remi:
    pkgrepo.managed:
    - humanname: Les RPM de remi pour Enterprise Linux 6 - $basearch
    - mirrorlist: http://rpms.famillecollet.com/enterprise/6/remi/mirror
    - comments:
        - '#Remi repo for mysql 5.6'
    - gpgcheck: 1
    - gpgkey: http://rpms.famillecollet.com/RPM-GPG-KEY-remi

GenieDB:
    pkgrepo.managed:
    - humanname:  GenieDB Packages
    - baseurl: http://packages.geniedb.com/v2/centos/stable
    - gpgcheck: 0

cloudfabric2:
  pkg:
    - installed
    - reload_modules: true
    - require:
      - pkgrepo: GenieDB
      - pkgrepo: remi
      - file: /etc/mysql/conf.d/geniedb.cnf
    - require_in:
      - service: mysqld

update_subscriptions:
  module.wait:
    - connection_args:
        connection_host: 'localhost'
        connection_user: 'root'
        connection_pass: ''
        connection_port: {{ pillar['dbaas_api']['cluster']['port'] }}
        connection_db: ''
    - name: mysql.query
    - database: test
    - query: SET GLOBAL geniedb_subscriptions="{{pillar['dbaas_api']['cluster']['subscriptions']}}";
    - watch:
      - file: /etc/mysql/conf.d/geniedb.cnf

/etc/mysql/conf.d/geniedb.cnf:
  file.managed:
    - show_diff: False
    - makedirs: True
    - source: salt://geniedb/geniedb.cnf
    - template: jinja
    - require_in:
      - service: mysqld

/usr/local/bin/cf-notify-error:
  file.managed:
    - show_diff: False
    - makedirs: True
    - source: salt://geniedb/cf-notify-error
    - mode: 755
    - template: jinja
