#!/bin/bash

#starts with parameters for database name and root password set in couchdb-template.sh
echo
echo "openstack_start: $OPENSTACK_START"
echo "openstack_restart: $OPENSTACK_RESTART"
echo "openstack_stop: $OPENSTACK_STOP"
echo "docker_start: $DOCKER_START"
echo "docker_restart: $DOCKER_RESTART"
echo "docker_stop: $DOCKER_STOP"
echo
echo "db_user = ${DB_USER}"
echo "environment = ${ENVIRONMENT}"
echo "repository_couchdb = ${REPOSITORY_COUCHDB}"
echo "check_path = ${CHECK_PATH}"
echo

mkdir -p $DATADIR
chown -R couchdb:couchdb $DATADIR

apt-get update

#installing to manage source repositories
apt-get install software-properties-common -y --force-yes

#PPA that will fetch latest CouchDB version from the repository
add-apt-repository ppa:couchdb/stable -y --force-yes

apt-get update

apt-get remove couchdb couchdb-bin couchdb-common -yf

#install CouchDB
apt-get install couchdb -y --force-yes

#retrieve basic information by CouchDB
curl localhost:5984


# for openstack as environment
if [ "$ENVIRONMENT" = 'openstack' ]; then
 $OPENSTACK_STOP
fi
# for docker as environment
if [ "$ENVIRONMENT" = 'docker' ]; then
 $DOCKER_STOP
fi
