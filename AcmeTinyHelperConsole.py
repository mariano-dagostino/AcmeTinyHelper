import sys
import getopt

from AcmeTinyHelper import SSLManager

class AcmeTinyHelperConsole(object):

    def __init__(self):
        self.path = None
        self.domains = None
        self.acme_tiny_path = '/bin/acme-tiny.py'
        self.challenge_path = '/var/www/challenges'
        self.execute = False

    def parseParams(self, params):
        for param, value in params:
            if param == '--path':
                self.path = value
            elif param == '--domains':
                self.domains = value.split(',')
            elif param == '--acme-tiny-path':
                self.acme_tiny_path = value
            elif param == '--challenge-path':
                self.challenge_path = value
            elif param == '--execute':
                self.execute = True


    def checkMissingParams(self):
        if self.path is None or self.domains is None:
            print "Some parameters are missing"
            print self.usage()
            sys.exit(2)

    def appParams(self):
        return [
          'path=',
          'domains=',
          'acme-tiny-path=',
          'challenge-path='
          'execute'
        ]


    def actions(self):
        return ('new', 'renew', 'help', )


    def usage(self):
        usage = "Usage mode:\n\n" + \
                "python AcmeTinyHelper.py [new|renew] /path/to/ssl-certs " + \
                "'example.com,www.example.com' " + \
                "[--acme-tiny-path=/bin/acme-tiny.py " + \
                "--challenge-path=/var/www/letsencrypt-challenges]\n\n" + \
                "--path: Indicates where will be saved all the files\n\n" + \
                "--domains: A comma separated list of domains (example: 'example.com,www.example.com')\n\n" + \
                "--acme-tiny-path: The path where acme-tiny.py is located (defaults to /bin/acme-tiny.py)\n\n" + \
                "--challenge-path: The directory where acme-tiny.py will write the challenge to authenticate the domain with letscrypt.org (defaults to /var/www/challenges)\n\n" + \
                "--execute: If this parameter is set, the script will execute all the commands instead of output them in the terminal as text.\n\n"

        return usage


    def invalidAction(self, action):
        valid_actions = ', '.join(self.actions())
        print "{action} is invalid. The only valid actions are: {valid_actions}".format(**locals())
        print self.usage()
        sys.exit(2)


    def invalidParams(self):
        print "Some parameters are not valid."
        print self.usage()
        sys.exit(2)


    def run(self, action, params):
        self.parseParams(params)

        manager = SSLManager(self.path,
                             self.domains,
                             self.acme_tiny_path,
                             self.challenge_path,
                             self.execute)
        if action == 'new':
            manager.newCertificate()

        if action == 'renew':
            manager.renewCertificate()

    def start(self):

        if sys.argv[1] == 'help':
            print self.usage()
            sys.exit(0)

        try:
            opts, args = getopt.getopt(sys.argv[2:], "", self.appParams())

            if sys.argv[1] not in self.actions():
                self.invalidAction(sys.argv[1])

            self.parseParams(opts)
            self.checkMissingParams()
            self.run(sys.argv[1], opts)

        except getopt.GetoptError:
            self.invalidParams()


if __name__ == '__main__':
    console = AcmeTinyHelperConsole()
    console.start()
