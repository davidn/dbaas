aladdin:
  user.present:
    - shell: /bin/bash

AAAAB3NzaC1yc2EAAAADAQABAAABAQDm1Y6SUQHH2XrPjTDgfjR34UT61q7mLwH/lCKqMmjJM5KoAAZ2Acw4eWQRLoPYTBWpQYlkO88lrY/DGrDwCKPOwgEc3aqxoLVmtIzJQL1Hsv1Zgo/7FtMAe3ttEPGqg691sAdhYytY7W1bJxxZ6UqgJpJujjSKwGl/mlOsbysalF1vNMqkzRvCpT9BkMUjJDT/qpGP4avKQPK420BrAXikhe0lnYL4tkPB/RcXHjMWnpoLzm6LAOj+Nst+kL8Z6fQHdHXPADMhn4pa1tdTVymhKpVHOyR62KopP6BnOiR16Pcg4kD1iWu3//GdJZV25x5V/9Eb+Z8buA6sBhbx4JaD:

  ssh_auth:
    - present
    - user: aladdin
    - enc: ssh-rsa
    - require:
      - user: aladdin

/etc/sudoers:
  file.append:
    - text: |
        aladdin    ALL=(ALL)    NOPASSWD: ALL
