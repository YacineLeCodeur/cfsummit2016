import subprocess
import sys
import unittest

import docker_volume_service.executer


PY_VERSION = sys.version_info
if PY_VERSION >= (3, 0):
    import unittest.mock as mock

    BUILTIN = 'builtins'
else:
    import mock

    BUILTIN = '__builtin__'


class RestoreOldMountsTest(unittest.TestCase):
    @mock.patch('docker_volume_service.executer.DockerVolumeService.run',
                mock.Mock)
    def setUp(self):
        self.dvs = docker_volume_service.executer.DockerVolumeService(None)

    @mock.patch(BUILTIN + '.open', mock.mock_open(read_data=''))
    def test_empty_file(self):
        with self.assertRaises(StopIteration):
            self.dvs._restore_old_mounts()
        self.assertEqual(self.dvs._mount_points, set())

    @mock.patch(BUILTIN + '.open', mock.mock_open(read_data='\n'))
    def test_only_new_line(self):
        self.dvs._restore_old_mounts()
        self.assertEqual(self.dvs._mount_points, set())

    @mock.patch(BUILTIN + '.open', mock.mock_open(read_data='test'))
    def test_one_line_wo_new_line(self):
        with self.assertRaises(StopIteration):
            self.dvs._restore_old_mounts()
        self.assertEqual(self.dvs._mount_points, {'test'})

    @mock.patch(BUILTIN + '.open', mock.mock_open(read_data='test\n'))
    def test_one_line_with_new_line(self):
        with self.assertRaises(StopIteration):
            self.dvs._restore_old_mounts()
        self.assertEqual(self.dvs._mount_points, {'test'})

    @mock.patch(BUILTIN + '.open', mock.mock_open(read_data='test1\ntest2'))
    def test_two_lines_wo_new_line(self):
        with self.assertRaises(StopIteration):
            self.dvs._restore_old_mounts()
        self.assertEqual(self.dvs._mount_points, {'test1', 'test2'})

    @mock.patch(BUILTIN + '.open', mock.mock_open(read_data='test1\ntest2\n'))
    def test_two_lines_with_new_line(self):
        with self.assertRaises(StopIteration):
            self.dvs._restore_old_mounts()
        self.assertEqual(self.dvs._mount_points, {'test1', 'test2'})


class SaveMountPointsTest(unittest.TestCase):
    @mock.patch('docker_volume_service.executer.DockerVolumeService.run',
                mock.Mock)
    def setUp(self):
        self.dvs = docker_volume_service.executer.DockerVolumeService(None)
        self.m = mock.MagicMock()

    def test_no_mount_points(self):
        self.dvs._mount_points = {}
        with mock.patch(BUILTIN + '.open', mock.mock_open(mock=self.m)):
            self.dvs._save_mount_points_set()
        self.m().writelines.assert_not_called()

    def test_one_mount_point(self):
        self.dvs._mount_points = {'test'}
        with mock.patch(BUILTIN + '.open', mock.mock_open(mock=self.m)):
            self.dvs._save_mount_points_set()
        self.m().writelines.assert_called_once_with('test\n')

    def test_two_mount_point(self):
        self.dvs._mount_points = {'test1', 'test2'}
        with mock.patch(BUILTIN + '.open', mock.mock_open(mock=self.m)):
            self.dvs._save_mount_points_set()
        self.assertEqual(self.m().writelines.call_count, 2)
        self.m().writelines.assert_has_calls(
            calls=[mock.call('test1\n'), mock.call('test2\n')],
            any_order=True,
        )


class GetNextLoopDeviceNumberTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_no_loop_devices(self):
        subprocess.check_output = mock.Mock(return_value='')
        self.assertEqual(
            docker_volume_service.executer.get_next_loop_device_number(),
            '0')

    def test_one_loop_device(self):
        subprocess.check_output = mock.Mock(return_value='loop0')
        self.assertEqual(
            docker_volume_service.executer.get_next_loop_device_number(),
            '1')

    def test_one_random_loop_device(self):
        subprocess.check_output = mock.Mock(return_value='loop123')
        self.assertEqual(
            docker_volume_service.executer.get_next_loop_device_number(),
            '0')

    def test_two_loop_devices(self):
        subprocess.check_output = mock.Mock(return_value='loop0\nloop1')
        self.assertEqual(
            docker_volume_service.executer.get_next_loop_device_number(),
            '2')

    def test_two_random_loop_devices(self):
        subprocess.check_output = mock.Mock(return_value='loop123\nloop789')
        self.assertEqual(
            docker_volume_service.executer.get_next_loop_device_number(),
            '0')


class MainTest(unittest.TestCase):
    @mock.patch('docker_volume_service.executer.DockerVolumeService',
                mock.MagicMock())
    def test_main_wo_args(self):
        sys.argv = []
        with mock.patch('sys.exit',
                        mock.Mock(side_effect=Exception('sys.exit')),
                        ) as sys_exit_mock:
            with self.assertRaisesRegexp(Exception, 'sys.exit'):
                docker_volume_service.executer.main()
        self.once_with = sys_exit_mock.assert_called_once_with(2)

    @mock.patch('docker_volume_service.executer.DockerVolumeService',
                mock.MagicMock())
    def test_main_with_h_args(self):
        sys.argv = ['', '-h']
        with mock.patch('sys.exit',
                        mock.Mock(side_effect=Exception('sys.exit')),
                        ) as sys_exit_mock:
            with self.assertRaisesRegexp(Exception, 'sys.exit'):
                docker_volume_service.executer.main()
            sys_exit_mock.assert_called_once_with()

    @mock.patch('docker_volume_service.executer.DockerVolumeService',
                mock.MagicMock())
    def test_main_with_help_args(self):
        sys.argv = ['', '--help']
        with mock.patch('sys.exit',
                        mock.Mock(side_effect=Exception('sys.exit')),
                        ) as sys_exit_mock:
            with self.assertRaisesRegexp(Exception, 'sys.exit'):
                docker_volume_service.executer.main()
            sys_exit_mock.assert_called_once_with()

    def test_main_with_b_args(self):
        sys.argv = ['', '-b', 'localhost']
        with mock.patch('docker_volume_service.executer.DockerVolumeService',
                        mock.MagicMock()) as dvs:
            docker_volume_service.executer.main()
            dvs.assert_called_once_with('localhost', '/var/run/dvs.pid', False)

    def test_main_with_broker_args(self):
        sys.argv = ['', '--broker=localhost']
        with mock.patch('docker_volume_service.executer.DockerVolumeService',
                        mock.MagicMock()) as dvs:
            docker_volume_service.executer.main()
            dvs.assert_called_once_with('localhost', '/var/run/dvs.pid', False)

    def test_main_with_b_and_d_args(self):
        sys.argv = ['', '-b', 'localhost', '-d']
        with mock.patch('docker_volume_service.executer.DockerVolumeService',
                        mock.MagicMock()) as dvs:
            docker_volume_service.executer.main()
            dvs.assert_called_once_with('localhost', '/var/run/dvs.pid', True)

    def test_main_with_b_and_daemonize_args(self):
        sys.argv = ['', '-b', 'localhost', '--daemon']
        with mock.patch('docker_volume_service.executer.DockerVolumeService',
                        mock.MagicMock()) as dvs:
            docker_volume_service.executer.main()
            dvs.assert_called_once_with('localhost', '/var/run/dvs.pid', True)


if __name__ == '__main__':
    unittest.main()
