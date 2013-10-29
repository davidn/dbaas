{% if data['act'] == 'accept' %}
highstate_run:
  cmd.state.highstate:
    - tgt: {{ data['id'] }}
{%endif%}
