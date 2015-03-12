import os
import sys
import time
import unittest


# FIXME
# It would be probably better if the port was randomly selected.
# https://fedorahosted.org/libuser/browser/tests/alloc_port.c
srv_host = 'localhost'
srv_port = 64000


def find_openssl():
    if os.name == 'nt' or sys.platform == 'cygwin':
        openssl = 'openssl.exe'
    else:
        openssl = 'openssl'

    plist = os.environ['PATH'].split(os.pathsep)
    for p in plist:
        try:
            dir = os.listdir(p)
            if openssl in dir:
                return True
        except:
            pass
    return False


class PosixSSLClientTestCase(unittest.TestCase):

    openssl_in_path = find_openssl()

    def start_server(self, args):
        if not self.openssl_in_path:
            raise Exception('openssl command not in PATH')

        pid = os.fork()
        if pid == 0:
            # openssl must be started in the tests directory for it
            # to find the .pem files
            os.chdir('tests')
            try:
                os.execvp('openssl', args)
            finally:
                os.chdir('..')

        else:
            time.sleep(sleepTime)
            return pid

    def stop_server(self, pid):
        os.kill(pid, 1)
        os.waitpid(pid, 0)

    def http_get(self, s):
        s.send('GET / HTTP/1.0\n\n')
        resp = ''
        while 1:
            try:
                r = s.recv(4096)
                if not r:
                    break
            except SSL.SSLError: # s_server throws an 'unexpected eof'...
                break
            resp = resp + r
        return resp

    def setUp(self):
        self.srv_host = srv_host
        self.srv_port = srv_port
        self.srv_addr = (srv_host, srv_port)
        self.srv_url = 'https://%s:%s/' % (srv_host, srv_port)
        self.args = ['s_server', '-quiet', '-www',
                     #'-cert', 'server.pem', Implicitly using this
                     '-accept', str(self.srv_port)]

    def tearDown(self):
        global srv_port
        srv_port = srv_port - 1
