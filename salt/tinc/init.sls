/etc/tinc/cf/tinc.conf:
  file.managed:
    - makedirs: True
    - source: salt://tinc/tinc.conf
    - template: jinja

/etc/tinc/cf/tinc-up:
  file.managed:
    - makedirs: True
    - source: salt://tinc/tinc-up
    - mode: 755
    - template: jinja

/etc/tinc/cf/rsa_key.priv:
  file.managed:
    - makedirs: True
    - source: salt://tinc/rsa_key.priv
    - mode: 600
    - template: jinja

{% for node in pillar['dbaas_api']['cluster']['nodes'] %}
/etc/tinc/cf/hosts/node_{{ node['nid'] }}:
  file.managed:
    - makedirs: True
    - source: salt://tinc/node_
    - template: jinja
    - defaults:
        node: {{ node }}
{% endfor %}

tinc:
  pkg:
    - installed
  service:
    - running
    - enable: True
    - reload: True
    - require:
      - pkg: tinc
    - watch:
      - file: /etc/tinc/cf/tinc.conf
      - file: /etc/tinc/cf/tinc-up
      - file: /etc/tinc/cf/rsa_key.priv
{% for node in pillar['dbaas_api']['cluster']['nodes'] %}
      - file: /etc/tinc/cf/hosts/node_{{ node['nid'] }}
{% endfor %}
