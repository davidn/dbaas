/etc/tinc/cf/tinc.conf:
  file.managed:
    - makedirs: True
    - source: salt://tinc/tinc.conf
    - template: jinja

/etc/tinc/cf/tinc-up:
  file.managed:
    - makedirs: True
    - source: salt://tinc/tinc-up
    - template: jinja

/etc/tinc/cf/rsa_key.priv:
  file.managed:
    - makedirs: True
    - source: salt://tinc/rsa_key.priv
    - template: jinja

{% for node in pillar['dbaas_api']['cluster']['nodes'] %}
/etc/tinc/cf/node_{{ node['nid'] }}:
  file.managed:
    - makedirs: True
    - source: salt://tinc/node_
    - template: jinja
    - defaults:
        node: {{ node }}
{% endfor %}

tinc:
  service:
    - running
  package:
    - installed
