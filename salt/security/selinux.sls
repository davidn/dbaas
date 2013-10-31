{% if salt['cmd.run']("getenforce") != "Disabled" %}
permissive:
  selinux.mode
{% endif %}
