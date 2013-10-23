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
    - require_in:
      -pkg: cloudfabric2

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
