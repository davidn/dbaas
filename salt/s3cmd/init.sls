s3cmd:
  pkg.installed

/root/.s3cfg:
  file.managed:
    - show_diff: False
    - source: salt://s3cmd/s3cfg
    - template: jinja
