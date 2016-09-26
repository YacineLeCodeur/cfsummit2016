#!/bin/bash

###################### Variables for standalone usage #########################
#
## ENVIRONMENT ##
#     1. for OpenStack and all full Linux-Environments:   "openstack"
#     2. for Docker as Environment:                       "docker"
#
## LOG_HOST and LOG_PORT ##
#     - this must be the IP and the Port on the external Logging-Host
#
## DB_PASSWORD & DB_USER ##
#     - is for the couchdb serveradministrator
#     - the password is used for monit with the username "monit"
#
export db_user="evoila"
export db_password="evoila"
export log_host="172.24.102.12"
export log_port="5002"
export log_protocol="tcp"


############ You have to copy the following lines into your script ############

#### Configuration Part - For environment and repository branch ####

## ENVIRONMENT - Change the variable for chose of the environment. Your Options are:
#     1. for OpenStack and all full Linux-Environments:   "openstack"
#     2. for Docker as Environment:                       "docker"
export environment="openstack"

# Change the variable for chose of branch in the repository. Your Options are:
#     1. master-branch:       "HEAD"
#     2. testing-branch:      "testing"
#     3. development-branch:  "development"
export REPOSITORY_BRANCH="HEAD"

export REPOSITORY_URL="https://bitbucket.org/evoila-boxer/deployment-scripts-docker-openstack/raw"

# describes the sub-path to the installed service and the sub-path to the monit scrips
export SERVICE_PATH="couchdb"
export MONIT_PATH="monit"


#### Static Part - No changes necessary ####

# describes the path to the used repositories using the variables above
export REPOSITORY_MAIN="$REPOSITORY_URL/$REPOSITORY_BRANCH"
export REPOSITORY_COUCHDB="$REPOSITORY_URL/$REPOSITORY_BRANCH/$SERVICE_PATH"
export REPOSITORY_MONIT="$REPOSITORY_URL/$REPOSITORY_BRANCH/$MONIT_PATH"

# downloads and executes the template for the installation of the service
wget $REPOSITORY_COUCHDB/couchdb-template.sh --no-cache
chmod +x couchdb-template.sh
./couchdb-template.sh -u $db_user -p $db_password -e $environment -l $log_host -m $log_port -c $log_protocol
