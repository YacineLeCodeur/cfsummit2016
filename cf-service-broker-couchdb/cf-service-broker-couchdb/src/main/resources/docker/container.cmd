export REPOSITORY_REDIS=$repo_service &&
export REPOSITORY_MAIN=$repo_main &&
apt-get update &&
apt-get install -y wget &&
wget $repo_service/couchdb-template.sh --no-cache &&
chmod +x couchdb-template.sh &&
./couchdb-template.sh -u $db_user -p $db_password -e docker -l $log_host -m $log_port -c $log_protocol
