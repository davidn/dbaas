highstate_run:
  cmd.state.highstate:
    - tgt: {{ data['dns_name'] }}
