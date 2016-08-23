# !/usr/bin/env python 2.X.X

import sys
import os
import time
import atexit

class Daemon(object):

    def __init__(self, pidfile):
        self.pidfile = pidfile


    def daemonize(self):
        try:
            pid = os.fork()
            if pid > 0:
                # Exit first parent
                sys.exit(0)
        except OSError,e:
            sys.exit(1)

        # Decouple from parent environment
        os.chdir('/')
        os.setsid()
        os.umask(0)

        # Do second fork
        try:
            pid = os.fork()
            if pid > 0:
                # Exit from second parent
                sys.exit(0)
        except OSError as e:
            sys.exit(1)

        # Redirect standard file descriptors
        sys.stdout.flush()
        sys.stderr.flush()
        si = open(os.devnull, 'r')
        so = open(os.devnull, 'a+')
        se = open(os.devnull, 'a+')

        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())

        # register exit clear function
        atexit.register(self.cleanpid)

        pid = str(os.getpid())
        fp = open(self.pidfile, 'w+')
        fp.write(pid)
        fp.close()


    def cleanpid(self):
        os.remove(self.pidfile)

    def start(self):
        try:
            fp = open(self.pidfile, 'r')
            pid = fp.read()
            fp.close()
        except IOError as e:
            pid = None
        except SystemExit:
            pid = None

        if pid:
            print('python daemon already runing !!!')
            sys.exit(1)

        print('Daemon starting.....');
        self.daemonize()
        self.run()

    def run(self):
        raise Exception('do something...')