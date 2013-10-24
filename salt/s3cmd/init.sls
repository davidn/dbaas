s3cmd:
  package.installed

/root/.s3cfg:
  file.managed:
    - source: salt://s3cmd/s3cfg
    - template: jinja
