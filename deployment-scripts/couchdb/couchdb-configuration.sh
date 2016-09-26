#!/bin/bash
echo
echo "### Starting configuration of CouchDB ###"
echo

#starts with parameters for database name and root password set in mysql-template.sh
echo "db_user = ${DB_USER}"
echo "datadir = ${DATADIR}"
echo "config_dir = ${CONFIG}"
echo "environment = ${ENVIRONMENT}"
echo "db_user = ${DB_USER}"

#Changes for security reasons
#Changes ownership of the CouchDB directories
chown -R couchdb:couchdb /usr/lib/couchdb /usr/share/couchdb /etc/couchdb /usr/bin/couchdb
#Changes permission of the CouchDB directories
chmod -R 0770 /usr/lib/couchdb /usr/share/couchdb /etc/couchdb /usr/bin/couchdb $DATADIR

# for openstack as environment
if [ "$ENVIRONMENT" = 'openstack' ]; then
 $OPENSTACK_START
fi
# for docker as environment
if [ "$ENVIRONMENT" = 'docker' ]; then
 $DOCKER_START
fi

echo "; CouchDB CUSTOM Configuration Settings

; Custom settings should be made in this file. They will override settings
; in default.ini, but unlike changes made to default.ini, this file won't be
; overwritten on server upgrade.


[httpd]
port = 5984
bind_address = 0.0.0.0
authentication_handlers = {couch_httpd_auth, default_authentication_handler}

[couch_httpd_auth]
require_valid_user = true

[admins]
$DB_USER = $DB_PASSWORD

[couchdb]
database_dir = /var/lib/couchdb" > /etc/couchdb/local.d/custom.ini

#adding custom config file to couchdb configuration files chain
#couchdb -A $CONFIG

#echo
#echo "This are the used configuration files:"
#couchdb -c
#echo

#restarting couchdb for hashing password in config
# for openstack as environment
if [ "$ENVIRONMENT" = 'openstack' ]; then
 $OPENSTACK_RESTART
fi
# for docker as environment
if [ "$ENVIRONMENT" = 'docker' ]; then
 $DOCKER_RESTART
fi

#stopping couchdb after initial configuration
# for openstack as environment
if [ "$ENVIRONMENT" = 'openstack' ]; then
 $OPENSTACK_STOP
fi
# for docker as environment
if [ "$ENVIRONMENT" = 'docker' ]; then
 $DOCKER_STOP
fi
