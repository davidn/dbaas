highstate_run:
  cmd.state.highstate:
{% for node in data['nodes'] %}
    - tgt: {{ node['dns_name'] }}
{% endfor %}
