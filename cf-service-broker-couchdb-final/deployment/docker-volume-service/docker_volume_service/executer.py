#!/usr/bin/env python
"""Copyright [2016] [Dennis Mueller]

Licensed under the Apache License, Version 2.0 (the 'License');
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an 'AS IS' BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

The Docker Volume Service executable
"""
import ast
import getopt
import logging
import os.path
import socket
import subprocess
import sys

import paho.mqtt.client

import docker_volume_service.base_daemon


logging.basicConfig(
    level=logging.DEBUG,
    # filename='/var/log/dvs.log',
    format='%(asctime)s [%(levelname)s] - %(message)s'
)
LOG = logging.getLogger(__name__)
DOCKER_TOPIC = 'docker'
SIP_TOPIC = 'sip'
VOLUMES_TOPIC = 'volumes'
JOBS_TOPIC = 'jobs'
MOUNTS_DATA = 'mounts.data'
NODE_NAME = socket.gethostname()
HELP_MESSAGE = \
    """dvs [-d] -b <MQTT broker address>'
Usage:
-b, --broker=   The Broker to connect to
-d, --daemon    If you want to start this app as daemon"""


class DockerVolumeService(docker_volume_service.base_daemon.Daemon):
    """The Docker Volume Service"""

    def __init__(self, mqtt_broker_address, pid_file=None, daemonize=False):
        self._client = paho.mqtt.client.Client()
        self._mount_points = set()
        self.mqtt_broker_address = mqtt_broker_address
        if daemonize:
            super(DockerVolumeService, self).__init__(
                pidfile=pid_file
            )
            self.start()
        else:
            self.run()

    def run(self):
        """Starts the Docker Volume Service by listening on a mqtt broker"""
        try:
            self._restore_old_mounts()
            self._connect(self.mqtt_broker_address, 1883, 60)
            LOG.info(
                'Connected to ' + self.mqtt_broker_address +
                ' at 1883 as ' + NODE_NAME
            )
            self._client.loop_forever()
        except Exception as exception:
            LOG.error(exception)

    def _on_connect(self, client, userdata, flags, result_code):
        """on_connect function for the paho.mqtt.client.Client

        Subscribe to the topic <DOCKER_TOPIC>/<NODE_NAME>/<VOLUMES_TOPIC>/#
        with Quality of Service Level 2 (message is always delivered exactly
        once)
        """
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed
        topic = DOCKER_TOPIC + '/' + NODE_NAME + '/' + VOLUMES_TOPIC + '/#'
        LOG.info('Service subscribes on ' + topic)
        self._client.subscribe(
            topic=topic,
            qos=2,
        )

    def _restore_old_mounts(self):
        """Mount all images which are stored in _mount_points"""
        self._read_moint_points_set()
        for mount_point in self._mount_points:
            self._mount_image_by_mount_point(mount_point)

    def _read_moint_points_set(self):
        """Store all mount points in _mount_points set from saved data"""
        self._mount_points = set()
        if not os.path.isfile(MOUNTS_DATA):
            with open(MOUNTS_DATA, 'w+') as new_file:
                new_file.write('\n')
        with open(MOUNTS_DATA, 'r+', ) as mount_points:
            mount_point = mount_points.readline().replace('\n', '')
            while mount_point != '':
                self._mount_points.add(mount_point.replace('\n', ''))
                mount_point = mount_points.readline()

    def _save_mount_points_set(self):
        """Save the _mount_points set in an external file"""
        with open(MOUNTS_DATA, 'w') as mount_data_file:
            for mount_point in self._mount_points:
                mount_data_file.writelines(mount_point + '\n')

    def _send_job_status(self, client, sender_id, job_id, status):
        """Send via client to a sender the status of the job with the job_id"""
        job_payload = {
            'jobId': job_id,
            'status': status
        }
        topic = \
            DOCKER_TOPIC + '/' + SIP_TOPIC + '/' + sender_id + '/' + JOBS_TOPIC
        client.publish(
            topic=topic,
            payload=job_payload.__str__(),
            qos=2,
        )

    @staticmethod
    def _get_image_file_path_by_mount_point(mount_point):
        """Add default suffix .img to the mount point as image file name

        :param mount_point:
        :return:
        """
        return mount_point + '.img'

    def _create_new_image_file(self, mount_point, size):
        """

        :param mount_point:
        :param size:
        :return:
        """
        image_file = DockerVolumeService\
            ._get_image_file_path_by_mount_point(mount_point)
        subprocess.call(['touch', image_file])
        LOG.debug('touch ' + image_file)
        subprocess.call(['truncate', '-s', size + 'M', image_file])
        LOG.debug('truncate -s ' + size + 'M ' + image_file)
        subprocess.call(['mkfs.ext2', '-F', '-m', '0', image_file])
        LOG.debug('mkfs.ext2 -F -m 0 ' + image_file)

    def _mount_image_by_mount_point(self, mount_point):
        loop_device_number = get_next_loop_device_number()
        loop_device_path = '/dev/loop' + loop_device_number
        image_file = DockerVolumeService\
            ._get_image_file_path_by_mount_point(mount_point)

        subprocess.call(
            ['sudo', 'mknod', '-m', '660', loop_device_path, 'b', '7',
             loop_device_number])
        LOG.debug(
            'sudo mknod -m 660 ' + loop_device_path + ' b 7 ' +
            loop_device_number)
        subprocess.call(['sudo', 'losetup', loop_device_path, image_file])
        LOG.debug('sudo losetup ' + loop_device_path + ' ' + image_file)
        subprocess.call(['mkdir', mount_point])
        LOG.debug('mkdir ' + mount_point)
        subprocess.call(['sudo', 'mount', loop_device_path, mount_point])
        LOG.debug('sudo mount ' + loop_device_path + ' ' + mount_point)
        subprocess.call(['sudo', 'rm', '-rf', mount_point + '/lost+found'])
        LOG.debug('sudo rm -rf ' + mount_point + '/lost+found')

    def _umount_and_delete(self, mount_point):
        image_file = DockerVolumeService\
            ._get_image_file_path_by_mount_point(mount_point)

        loop_device_path = \
            str(
                subprocess.check_output(['losetup', '-j', image_file])
            ).split(': ')[0]
        subprocess.call(['sudo', 'umount', mount_point])
        LOG.debug('sudo umount ' + mount_point)
        subprocess.call(['sudo', 'rm', image_file])
        LOG.debug('sudo rm ' + image_file)
        subprocess.call(['sudo', 'losetup', '-d', loop_device_path])
        LOG.debug('sudo losetup -d ' + loop_device_path)
        subprocess.call(['sudo', 'rm', loop_device_path])
        LOG.debug('sudo rm ' + loop_device_path)

    def _save_mount_point(self, mount_point):
        self._mount_points.add(mount_point)
        self._save_mount_points_set()

    def _delete_mount_point(self, mount_point):
        self._mount_points.remove(mount_point)
        self._save_mount_points_set()

    # The callback for when a PUBLISH message is received from the server.
    def _on_message(self, client, userdata, msg):
        topic = msg.topic.split('/')[-1]
        if topic == 'create':
            payload = ast.literal_eval(msg.payload)
            sender_id = payload['sipId']
            job_id = payload['jobId']

            self._send_job_status(client, sender_id, job_id, 'PENDING')

            mount_point = payload['mountPoint']
            size = str(payload['volumeSize'])

            self._create_new_image_file(mount_point, size)
            self._mount_image_by_mount_point(mount_point)
            self._save_mount_point(mount_point)
            self._send_job_status(client, sender_id, job_id, 'DONE')

            LOG.info('Job ' + job_id + ' done.')
            LOG.debug('Job payload was ' + str(payload))
        elif topic == 'delete':
            payload = ast.literal_eval(msg.payload)
            sender_id = payload['sipId']
            job_id = payload['jobId']

            self._send_job_status(client, sender_id, job_id, 'PENDING')

            mount_point = payload['mountPoint']

            self._umount_and_delete(mount_point)
            self._delete_mount_point(mount_point)
            self._send_job_status(client, sender_id, job_id, 'DONE')

    def _connect(self, host, port, keepalive, bind_address=''):
        self._client.on_connect = self._on_connect
        self._client.on_message = self._on_message
        self._client.connect(
            host=host,
            port=port,
            keepalive=keepalive,
            bind_address=bind_address
        )


def get_next_loop_device_number():
    """Get the next loop device number for this system

    Note: Maximum count of loop devices is 1048576
    """
    available_device_number = list(range(1048576))
    devices = str(subprocess.check_output(['ls', '/dev/'])).split('\n')
    for device in devices:
        if device.startswith('loop'):
            device_number = device.split('loop')[1]
            if device_number.isdigit():
                available_device_number.remove(int(device_number))
    return str(available_device_number[0])


def main():
    """Starts the Docker Volume Service"""
    daemonize = False
    mqtt_broker_address = None
    try:
        opts, args = getopt.getopt(
            args=sys.argv[1:],
            shortopts='b:dh',
            longopts=['broker=', 'daemon', 'help'])
    except getopt.GetoptError as exception:
        print(exception.msg)
        print(HELP_MESSAGE)
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print(HELP_MESSAGE)
            sys.exit()
        elif opt in ('-b', '--broker'):
            mqtt_broker_address = arg
        elif opt in ('-d', '--daemon'):
            daemonize = True
    if not mqtt_broker_address:
        print(HELP_MESSAGE)
        sys.exit(2)
    DockerVolumeService(mqtt_broker_address, '/var/run/dvs.pid', daemonize)


if __name__ == '__main__':
    main()
