ENDPOINT?=https://dbaas.geniedb.com:4000/api/
AUTH_ENDPOINT?=https://dbaas.geniedb.com:4000/api-token-auth/

all: dbaas.js

%: %.in
	sed 's!@ENDPOINT@!$(ENDPOINT)!g; s!@AUTH_ENDPOINT@!$(AUTH_ENDPOINT)!g' < $< > $@
