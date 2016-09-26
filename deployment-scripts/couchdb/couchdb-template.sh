#!/bin/bash

export DATADIR=/data/couchdb
#export CONFIG=/data/couchdbconfig

# start/stop commands for different environments
export OPENSTACK_START="start couchdb"
export OPENSTACK_RESTART="restart couchdb"
export OPENSTACK_STOP="stop couchdb"
export DOCKER_START=""
export DOCKER_RESTART=""
export DOCKER_STOP=""

#path used to check if service is installed
export CHECK_PATH=$DATADIR

#parameters for vhost, user and password used in the following scripts
usage() { echo "Usage: $0 [-u <string>] [-p <string>] [-e <string>] [-l <string>] [-m <string>] [-c <string>] " 1>&2; exit 1; }

while getopts ":u:p:e:l:m:c:" o; do
    case "${o}" in
        u)
            DB_USER=${OPTARG}
            ;;
        p)
            DB_PASSWORD=${OPTARG}
            ;;
        e)
            ENVIRONMENT=${OPTARG}
            ;;
        l)
            LOG_HOST=${OPTARG}
            ;;
        m)
            LOG_PORT=${OPTARG}
            ;;
        c)
            LOG_PROTOCOL=${OPTARG}
            ;;
        *)
            usage
            ;;
    esac
done
shift $((OPTIND-1))

if [ -z "${DB_USER}" ] ||[ -z "${DB_PASSWORD}" ] || [ -z "${ENVIRONMENT}" ] || [ -z "${LOG_HOST}" ] || [ -z "${LOG_PORT}" ] || [ -z "${LOG_PROTOCOL}" ]; then
    usage
fi


# export for following scripts
export ENVIRONMENT=${ENVIRONMENT}
export DB_USER=${DB_USER}
export DB_PASSWORD=${DB_PASSWORD}
export LOG_HOST=${LOG_HOST}
export LOG_PORT=${LOG_PORT}
export LOG_PROTOCOL=${LOG_PROTOCOL}

echo "environment = ${ENVIRONMENT}"
echo "log_host=${LOG_HOST}"
echo "log_port=${LOG_PORT}"
echo "log_protocol=${LOG_PROTOCOL}"
echo "repository_couchdb = ${REPOSITORY_COUCHDB}"
echo "check_path = ${CHECK_PATH}"


# checks if service is installed
if [ -a $CHECK_PATH* ]; then
    # executes script for startup of couchdb
    chmod +x couchdb-run.sh
    ./couchdb-run.sh
else
    # loads and executes script for logging to a (central) logging instance
    wget $REPOSITORY_COUCHDB/couchdb-logging.sh --no-cache
    chmod +x couchdb-logging.sh
    ./couchdb-logging.sh

    # loads and executes script for automatic installation of couchdb
    wget $REPOSITORY_COUCHDB/couchdb-install.sh --no-cache
    chmod +x couchdb-install.sh
    ./couchdb-install.sh

    # loads and executes script for configuration of couchdb
    wget $REPOSITORY_COUCHDB/couchdb-configuration.sh
    chmod +x couchdb-configuration.sh
    ./couchdb-configuration.sh

    # loads includes for the monit controlfile for this database
#    mkdir -p /etc/monit.d/
#    wget $REPOSITORY_COUCHDB/couchdb-monitrc -P /etc/monit.d/

    # loads and executes script for startup of couchdb
    wget $REPOSITORY_COUCHDB/couchdb-run.sh --no-cache
    chmod +x couchdb-run.sh
    ./couchdb-run.sh
fi

# installs monit for openstack as environment
#if [ "$ENVIRONMENT" = 'openstack' ]; then
#  export REPOSITORY_MONIT="${REPOSITORY_MONIT}"
#  wget $REPOSITORY_MONIT/monit-template.sh --no-cache
#  chmod +x monit-template.sh
#  ./monit-template.sh -u monit -p ${DB_PASSWORD}
#fi
