
/etc/init.d/rsyncd:
  file.managed:
    - show_diff: False
    - source: salt://rsync/rsyncd.init
    - mode: 755
    - template: jinja

/etc/rsyncd.conf:
  file.managed:
    - show_diff: False
    - source: salt://rsync/rsyncd.conf
    - template: jinja

/usr/local/bin/pre-rsync:
  file.managed:
    - show_diff: False
    - makedirs: True
    - source: salt://rsync/pre-rsync
    - mode: 755
    - template: jinja

/usr/local/bin/post-rsync:
  file.managed:
    - show_diff: False
    - makedirs: True
    - source: salt://rsync/post-rsync
    - mode: 755
    - template: jinja

rsyncd:
  service:
    - running
    - enable: True
    - require:
      - file: /etc/init.d/rsyncd
      - file: /etc/rsyncd.conf
      - file: /usr/local/bin/pre-rsync
      - file: /usr/local/bin/post-rsync
