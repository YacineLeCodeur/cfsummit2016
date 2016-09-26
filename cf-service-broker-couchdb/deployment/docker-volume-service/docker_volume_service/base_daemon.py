"""Copyright [2016] [Dennis Mueller]

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

This module allows to execute code demonized
"""
import abc
import atexit
import os
import sys
import time
from signal import SIGTERM


class AlreadyDaemonized(Exception):
    """Raised when the process is already daemonized or pidfile exists"""

    pass


class Daemon(object):
    """A generic daemon class.

    Usage: subclass the Daemon class and override the run() method
    """

    def __init__(self, pidfile, stdin='/dev/null', stdout='/dev/null',
                 stderr='/dev/null'):
        """Set the pidfile path and the standard streams for in, out and err"""
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.pidfile = pidfile

    def _daemonize(self):
        """Do the UNIX double-fork magic

        see Stevens' "Advanced Programming in the UNIX Environment" for
        details (ISBN 0201563177)
        http://www.erlenstar.demon.co.uk/unix/faq_2.html#SEC16
        """
        try:
            pid = os.fork()
            if pid > 0:
                # exit first parent
                sys.exit(0)
        except OSError as exception:
            sys.stderr.write(
                "fork #1 failed: %d (%s)\n" % (
                    exception.errno,
                    exception.strerror
                ))
            sys.exit(1)

        # decouple from parent environment
        os.chdir("/")
        os.setsid()
        os.umask(0)

        # do second fork
        try:
            pid = os.fork()
            if pid > 0:
                # exit from second parent
                sys.exit(0)
        except OSError as exception:
            sys.stderr.write(
                "fork #2 failed: %d (%s)\n" % (
                    exception.errno,
                    exception.strerror)
            )
            sys.exit(1)

        # redirect standard file descriptors
        sys.stdout.flush()
        sys.stderr.flush()
        stdin = file(self.stdin, 'r')
        stdout = file(self.stdout, 'a+')
        stderr = file(self.stderr, 'a+', 0)
        os.dup2(stdin.fileno(), sys.stdin.fileno())
        os.dup2(stdout.fileno(), sys.stdout.fileno())
        os.dup2(stderr.fileno(), sys.stderr.fileno())

    def _create_pidfile(self):
        """Create the pidfile"""
        atexit.register(self._delelete_pidfile)
        pid = str(os.getpid())
        file(self.pidfile, 'w+').write("%s\n" % pid)

    def _delelete_pidfile(self):
        """Delete the pidfile"""
        os.remove(self.pidfile)

    def _is_pidfile_exists(self):
        """Checks if pidfile exists

        :return: Boolean -- True if pidfile exists
        """
        return os.path.isfile(self.pidfile)

    def start(self):
        """Start the daemon if no pidfile exists"""

        if self._is_pidfile_exists():
            raise AlreadyDaemonized('pidfile ' + self.pidfile +
                                    'already exist. Daemon already running?\n')

        self._daemonize()
        self._create_pidfile()
        self.run()

    def _get_pid(self):
        """Get the pid of the pidfile

        :return: String -- The pid read in pidfile. If pipfile not exist None.
        """
        if self._is_pidfile_exists():
            with open(self.pidfile) as pidfile:
                return pidfile.read().strip()

    def _kill_process_by_pidfile(self):
        """Kill the process which is read in the pidfile"""
        try:
            while True:
                os.kill(self._get_pid(), SIGTERM)
                time.sleep(0.1)
        except OSError as err:
            err = str(err)
            if err.find("No such process") > 0:
                if os.path.exists(self.pidfile):
                    os.remove(self.pidfile)
            else:
                print(str(err))
                sys.exit(1)

    def stop(self):
        """Stop the daemon"""
        if not self._is_pidfile_exists():
            message = "pidfile %s does not exist. Daemon not running?\n"
            sys.stderr.write(message % self.pidfile)
            return  # not an error in a restart

        self._kill_process_by_pidfile()

    def restart(self):
        """Restart the daemon"""
        self.stop()
        self.start()

    @abc.abstractmethod
    def run(self):
        """This method has to be implement by a subclass"""
        raise NotImplementedError
