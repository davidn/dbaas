ENDPOINT?=http://localhost:8000/api/
AUTH_ENDPOINT?=http://localhost:8000/api-token-auth/

all: dbaas.js

%: %.in
	sed 's!@ENDPOINT@!$(ENDPOINT)!g; s!@AUTH_ENDPOINT@!$(AUTH_ENDPOINT)!g' < $< > $@

.PHONY: dbaas.js
