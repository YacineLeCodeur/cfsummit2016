Docker Volume Service
===========================

## Overview
Because Docker does not support volume size limitation for containers this 
service was implemented. This service is a part of the 
[cloudfoundry-service-broker](https://github.com/evoila/cf-service-broker). 
Docker Volume Service connects to a MQTT Broker (e.g. [Erlang MQTT Broker] 
(http://emqtt.io)) and waits for volume-jobs which creates or deletes volumes
 connected to NOT running docker container. 

## Requirements
* python setuptools
* init/upstart or systemd
* This was tested with python2.7.6+ and Ubuntu14.04 and Ubuntu 16.04

## Installation
Download the repository and execute ```INSTALL.SH```.

## Usage
    dvs [option] -b <MQTT broker address>'
    Usage:
    -b, --broker=   The Broker to connect to
    -d, --daemon    If you want to start this app as daemon


## Configuration
How to change the MQTT broker addresse for the installed services

### init/upstart
Change the broker address in ```/etc/default/dvs```

### systemd
Change the MQTT_BROKER environment varibale in 
```/etc/systemd/system/multi-user.target.wants/dvs.service```

## Starting
The Docker Volume Service could be start after installation with ```dvs``` 
command, or as a service, if it is installed with the installation script.

## Queues
Docker Volume Service is subcribed to the 
\<DOCKER_TOPIC\>/\<NODE_NAME\>/\<VOLUMES_TOPIC\>/# queue (default: 
docker/<hostname>/volumes/#). A job requester is subcribed to the 
\<DOCKER_TOPIC\>/\<SIP_TOPIC\>/\<sender-identifier\>/\<JOBS_TOPIC\> queue 
(default: docker/sip/\<sender-identifier\>/jobs). At the docker volume 
service queue the decision of create or delete a volume will be made. Create 
jobs goes to the topic \<DOCKER_TOPIC\>/\<NODE_NAME>\/\<VOLUMES_TOPIC
\>/create, delete to \<DOCKER_TOPIC\>/\<NODE_NAME\>/\<VOLUMES_TOPIC\>/delete. 

### Payload
Payload are json string because of better reading and parsing. There are 
three types of payload, for each interaction, one is defined. 

#### Create job
This job creates a volume with a specific size and mount point. The Docker 
Volume Service will listen for those messages. On each request, Docker Volume
 Service will answer with a [Job Status](#job-status) message. 

Content

    job        : An id for the job which the sender has to wait for
    sipId      : The id of the sender for answering on its topic
    mountPount : This is the path where the new volume would be mounted
    volumeSize : This is the size in megabyte of the new volume


Example

    {
      "job" : "1234567890",
      "sipId" : "abcdefghi",
      "mountPount" : "/mnt",
      "volumeSize" : "5000"
    }

#### Delete job
This job deletes a volume at specific mount point. The Docker Volume Service 
will listen for those messages. On each request, Docker Volume Service will 
answer with a [Job Status](#job-status) message. 

Content

    job        : An id for the job which the sender has to wait for
    sipId      : The id of the sender for answering on its topic
    mountPount : This is the path where to mounted volume which would be deleted

Example

    {
      "job" : "1234567890",
      "sipId" : "abcdefghi",
      "mountPount" : "/mnt"
    }


#### Job status
This is the answer of create and delete a volume. When a job arrives the 
Dcoker Volume Service answers with a PENDING, after finishing the job Docker 
Volume Serivce sends a DONE to the sender with its job id. If the job breaks,
 no DONE message would be ever send, so the requester has to set a timeout 
 for finished jobs
 
Content

      job    : This is a jobId
      status : This is either PENDING or DONE

Example

    {
      "job" : "1234567890",
      "status" : "DONE"
    }

## Shell executions
At receiving a job the following commands will be executed by the Docker 
Volume Service at specefic job type:
### Create

    touch INAGEFILE
    truncate -s SIZE M IMAGEFILE
    mkfs.ext2 -F -m 0 IMAGEFILE
    sudo mknod -m 660 LOOPDEVICE\_PATH b 7 LOOPDEVICE\_NUMBER
    sudo losetup LOOPDEVICE\_PATH IMAGEFILE
    mkdir MOUNTPOINT
    sudo mount LOOPDEVICE\_PATH MOUNTPOINT
    sudo rm -R MOUNTPOUNT/lost+found


### Delete

    sudo umount MOUNTPOINT
    sudo rm IMAGEFILE
    sudo rm LOOPDEVICE\_PATH
