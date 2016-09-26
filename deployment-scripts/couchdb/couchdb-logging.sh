#!/bin/bash

echo "### Starting configuration for logging to (central) logging instance ... ###"

apt-get -y install rsyslog

export LOGGED_SERVICE="couchdb"
export LOG_FILE="/var/log/chouchdb/*"

echo "logging_host: = $LOG_HOST"
echo "logging_port: = $LOG_PORT"
echo "logging_protocol: = $LOG_PROTOCOL"

# adding additional configfile for sending logfiles from service with rsyslog to logging-instance
echo "# Default Settings

# Load Modules
module(load=\"imfile\")
module(load=\"omfwd\")
module(load=\"imuxsock\")

# rsyslog Templates

# rsyslog Input Modules
input(type=\"imfile\"
	 File=\"$LOG_FILE\"
	 Tag=\"\"
	 StateFile=\"\"
	 Severity=\"info\"
	 Facility=\"kern\")

# rsyslog RuleSets
# Default RuleSet
action(type=\"omfwd\"
	 Target=\"$LOG_HOST\"
	 Port=\"$LOG_PORT\"
	 Protocol=\"$LOG_PROTOCOL\")" > /etc/rsyslog.d/$LOGGED_SERVICE-rsyslog.conf

service rsyslog restart

echo
echo "Now logfiles will send to...
------
logging-host: $LOG_HOST
port: $LOG_PORT
protocol: $LOG_PROTOCOL
------"
echo
